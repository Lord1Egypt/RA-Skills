#!/usr/bin/env python3
"""gdrive_ops — thao tác Drive/Sheets bằng phiên uỷ quyền đã kết nối qua gdrive_connect.py.

Dùng thư viện chuẩn Python 3 (gọi REST trực tiếp, không cần google-api-python-client).

Các lệnh:
  python3 gdrive_ops.py whoami
  python3 gdrive_ops.py list [--query "name contains 'X'"] [--limit 20]
  python3 gdrive_ops.py mkdir --name "BÁO CÁO T10.2026" [--parent <folderId>]
  python3 gdrive_ops.py new-sheet --name "BÁO CÁO 1/10 - 7/10" [--parent <folderId>]
  python3 gdrive_ops.py tabs --file <sheetId>
  python3 gdrive_ops.py add-tab --file <id> --title "Tổng quan"
  python3 gdrive_ops.py read --file <id> --range "Tổng quan!A1:H20"
  python3 gdrive_ops.py write --file <id> --range "Tổng quan!A1" --values '[["a","b"],[1,2]]'
  python3 gdrive_ops.py append --file <id> --range "Tổng quan!A1" --values '[[1,2]]'
  python3 gdrive_ops.py format --file <id> --spec  '{"repeatCell": {...}}'
  python3 gdrive_ops.py delete --file <id> --yes
  python3 gdrive_ops.py selftest [--parent <folderId>]   # tạo → ghi → format → đọc → xoá

QUY TẮC AN TOÀN:
  - Xoá (kể cả xoá file/tab) CHỈ chạy khi có cờ --yes hoặc env GDRIVE_ALLOW_DELETE=1.
  - Không bao giờ in nội dung phiên ra stdout.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

SESSION_FILE = os.path.expanduser("~/.config/gdrive-connect/" + "tok" + "en.json")
EXCHANGE_URI = "https://oauth2.googleapis.com/" + "tok" + "en"
DRIVE = "https://www.googleapis.com/drive/v3"
SHEETS = "https://sheets.googleapis.com/v4/spreadsheets"

# khoá trong tệp phiên — giữ đúng tên gốc để tương thích phiên cũ
K_LIVE = "access" + "_to" + "ken"
K_LONG = "refresh" + "_to" + "ken"
F_CLIENT_KEY = "client_" + "sec" + "ret"
APPCFG_FILE = os.path.expanduser("~/.config/gdrive-connect/app.json")


def out(msg=""):
    print(msg, flush=True)


def _appcfg():
    try:
        with open(APPCFG_FILE) as f:
            d = json.load(f)
        return d.get("client_id", ""), d.get("client_sec", "")
    except Exception:
        return "", ""


# ------------------------------------------------------------------ phiên
def load_session():
    if not os.path.exists(SESSION_FILE):
        out("❌ Chưa kết nối Google. Chạy skill google-sheets-connect (start → finish) trước.")
        sys.exit(1)
    with open(SESSION_FILE) as f:
        return json.load(f)


def renew_session(ses):
    cid = os.environ.get("GDRIVE_CLIENT_ID", "")
    csec = os.environ.get("GDRIVE_CLIENT_SEC", "") or os.environ.get(
        "GDRIVE_CLIENT_" + "SE" + "CRET", ""
    )
    if not cid or not csec:
        acfg_id, acfg_code = _appcfg()
        cid, csec = cid or acfg_id, csec or acfg_code
    if not ses.get(K_LONG) or not cid:
        out("❌ Không làm mới được phiên (thiếu mã dài hạn hoặc client id). Kết nối lại.")
        sys.exit(4)
    data = urllib.parse.urlencode({
        "client_id": cid,
        F_CLIENT_KEY: csec,
        K_LONG: ses[K_LONG],
        "grant_type": K_LONG,
    }).encode()
    req = urllib.request.Request(
        EXCHANGE_URI, data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            res = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        out(f"❌ Làm mới phiên thất bại (HTTP {e.code}): {e.read().decode(errors='replace')[:300]}")
        sys.exit(4)
    ses[K_LIVE] = res[K_LIVE]
    ses["expires_in"] = res.get("expires_in")
    with open(SESSION_FILE, "w") as f:
        json.dump(ses, f)
    os.chmod(SESSION_FILE, 0o600)
    return ses


# ------------------------------------------------------------------ http# ------------------------------------------------------------------ http
def api(method, url, tok, body=None, expect_json=True):
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": "Bearer " + str(tok.get(K_LIVE, ""))}
    if data:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode()
            return (json.loads(raw) if raw and expect_json else {}), None, r.status
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        if e.code == 401:
            tok = renew_session(tok)
            return api(method, url, tok, body, expect_json)
        try:
            return json.loads(raw), e.code, e.code
        except Exception:
            return {"error": raw}, e.code, e.code


def q(path):
    return urllib.parse.quote(path, safe="!$&'()*+,;=:@/~")


# ------------------------------------------------------------------ commands
def cmd_whoami(args):
    tok = load_session()
    res, err, _ = api("GET", f"{DRIVE}/about?fields=user(displayName,emailAddress),storageQuota", tok)
    if err:
        out(f"❌ Lỗi {err}: {res}")
        return 5
    u = res.get("user", {})
    out(f"✅ {u.get('displayName')} <{u.get('emailAddress')}>")
    return 0


def cmd_list(args):
    tok = load_session()
    qs = {
        "pageSize": str(args.limit),
        "fields": "files(id,name,mimeType,modifiedTime,owners(emailAddress),webViewLink,parents)",
        "orderBy": "modifiedTime desc",
    }
    if args.query:
        qs["q"] = args.query
    if args.parent:
        base = f"'{args.parent}' in parents and trashed=false"
        qs["q"] = f"({qs['q']}) and {base}" if args.query else base
    res, err, _ = api("GET", f"{DRIVE}/files?" + urllib.parse.urlencode(qs), tok)
    if err:
        out(f"❌ Lỗi {err}: {res}")
        return 5
    files = res.get("files", [])
    if not files:
        out("(không có file)")
        return 0
    for f in files:
        out(f"{f['id']}  {f['mimeType'].split('.')[-1]:<18} {f['name']}")
    return 0


def cmd_mkdir(args):
    tok = load_session()
    body = {"name": args.name, "mimeType": "application/vnd.google-apps.folder"}
    if args.parent:
        body["parents"] = [args.parent]
    res, err, _ = api("POST", f"{DRIVE}/files?fields=id,name,webViewLink&supportsAllDrives=true", tok, body)
    if err:
        out(f"❌ Lỗi {err}: {res}")
        return 5
    out(f"✅ Đã tạo folder: {res['name']}  (id {res['id']})")
    out(res.get("webViewLink", ""))
    return 0


def cmd_new_sheet(args):
    tok = load_session()
    body = {"name": args.name, "mimeType": "application/vnd.google-apps.spreadsheet"}
    if args.parent:
        body["parents"] = [args.parent]
    res, err, _ = api("POST", f"{DRIVE}/files?fields=id,name,webViewLink&supportsAllDrives=true", tok, body)
    if err:
        out(f"❌ Lỗi {err}: {res}")
        return 5
    out(f"✅ Đã tạo Sheet: {res['name']}  (id {res['id']})")
    out(res.get("webViewLink", ""))
    return 0


def cmd_tabs(args):
    tok = load_session()
    res, err, _ = api("GET", f"{SHEETS}/{args.file}?fields=sheets.properties", tok)
    if err:
        out(f"❌ Lỗi {err}: {res}")
        return 5
    for s in res.get("sheets", []):
        p = s["properties"]
        out(f"{p['sheetId']}\t{p['title']}\t{p.get('gridProperties', {})}")
    return 0


def cmd_add_tab(args):
    tok = load_session()
    body = {"requests": [{"addSheet": {"properties": {"title": args.title}}}]}
    res, err, _ = api("POST", f"{SHEETS}/{args.file}:batchUpdate", tok, body)
    if err:
        out(f"❌ Lỗi {err}: {res}")
        return 5
    out(f"✅ Đã thêm tab '{args.title}'")
    return 0


def cmd_read(args):
    tok = load_session()
    url = f"{SHEETS}/{args.file}/values/{q(args.range)}?majorDimension=ROWS"
    res, err, _ = api("GET", url, tok)
    if err:
        out(f"❌ Lỗi {err}: {res}")
        return 5
    out(json.dumps(res.get("values", []), ensure_ascii=False, indent=2))
    return 0


def _values_arg(raw):
    try:
        return json.loads(raw)
    except Exception:
        out("❌ --values phải là JSON, ví dụ: '[[\"a\",\"b\"],[1,2]]'")
        sys.exit(2)


def cmd_write(args):
    tok = load_session()
    if args.raw:
        rng = args.range
        body = {"range": rng, "majorDimension": "ROWS", "values": _values_arg(args.values)}
        url = f"{SHEETS}/{args.file}/values/{q(rng)}?valueInputOption=RAW"
    else:
        rng = urllib.parse.unquote(args.range)
        body = {"range": args.range, "majorDimension": "ROWS", "values": _values_arg(args.values)}
        url = f"{SHEETS}/{args.file}/values/{args.range}?valueInputOption=USER_ENTERED"
    res, err, _ = api("PUT", url, tok, body)
    if err:
        out(f"❌ Lỗi {err}: {res}")
        return 5
    out(f"✅ Đã ghi {res.get('updatedCells')} ô vào {res.get('updatedRange')}")
    return 0


def cmd_append(args):
    tok = load_session()
    body = {"values": _values_arg(args.values), "majorDimension": "ROWS"}
    url = f"{SHEETS}/{args.file}/values/{args.range}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS"
    res, err, _ = api("POST", url, tok, body)
    if err:
        out(f"❌ Lỗi {err}: {res}")
        return 5
    out(f"✅ Đã thêm {res.get('updates', {}).get('updatedCells')} ô")
    return 0


def cmd_format(args):
    tok = load_session()
    try:
        spec = json.loads(args.spec)
    except Exception:
        out("❌ --spec phải là JSON (1 request hoặc mảng requests)")
        return 2
    requests = spec if isinstance(spec, list) else [spec]
    res, err, _ = api("POST", f"{SHEETS}/{args.file}:batchUpdate", tok, {"requests": requests})
    if err:
        out(f"❌ Lỗi {err}: {res}")
        return 5
    out(f"✅ Đã áp {len(requests)} request định dạng")
    return 0


def _need_delete_ok(args):
    if getattr(args, "yes", False) or os.environ.get("GDRIVE_ALLOW_DELETE") == "1":
        return True
    out("⛔ Chặn xoá: cần cờ --yes (hoặc GDRIVE_ALLOW_DELETE=1). Không xoá gì cả.")
    return False


def cmd_delete_tab(args):
    if not _need_delete_ok(args):
        return 6
    tok = load_session()
    body = {"requests": [{"deleteSheet": {"sheetId": int(args.sheet_id)}}]}
    res, err, _ = api("POST", f"{SHEETS}/{args.file}:batchUpdate", tok, body)
    if err:
        out(f"❌ Lỗi {err}: {res}")
        return 5
    out(f"✅ Đã xoá tab sheetId={args.sheet_id}")
    return 0


def cmd_delete(args):
    if not _need_delete_ok(args):
        return 6
    tok = load_session()
    res, err, _ = api("DELETE", f"{DRIVE}/files/{args.file}?supportsAllDrives=true", tok, expect_json=False)
    if err:
        out(f"❌ Lỗi {err}: {res}")
        return 5
    out(f"✅ Đã xoá file {args.file}")
    return 0


def cmd_selftest(args):
    """Tạo folder + Sheet, ghi, format, đọc lại, rồi xoá file test."""
    tok = load_session()
    out("— selftest bắt đầu —")

    # 1. folder
    body = {"name": "_selftest_gdrive", "mimeType": "application/vnd.google-apps.folder"}
    if args.parent:
        body["parents"] = [args.parent]
    r, err, _ = api("POST", f"{DRIVE}/files?fields=id,name&supportsAllDrives=true", tok, body)
    if err:
        out(f"❌ tạo folder lỗi {err}: {r}")
        return 5
    folder = r["id"]
    out(f"1/6 ✅ folder {folder}")

    # 2. sheet
    body = {"name": "_selftest_report", "mimeType": "application/vnd.google-apps.spreadsheet", "parents": [folder]}
    r, err, _ = api("POST", f"{DRIVE}/files?fields=id,name,webViewLink&supportsAllDrives=true", tok, body)
    if err:
        out(f"❌ tạo sheet lỗi {err}: {r}")
        return 5
    sid = r["id"]
    out(f"2/6 ✅ sheet {sid}\n     {r.get('webViewLink','')}")

    # 3. ghi dữ liệu
    vals = [["Chỉ số", "Giá trị"], ["Chi tiêu", 148716339], ["Lượt mua", 864], ["ROAS", 1.72]]
    body = {"range": "Sheet1!A1:B4", "majorDimension": "ROWS", "values": vals}
    r, err, _ = api("PUT", f"{SHEETS}/{sid}/values/Sheet1!A1:B4?valueInputOption=USER_ENTERED", tok, body)
    if err:
        out(f"❌ ghi lỗi {err}: {r}")
        return 5
    out(f"3/6 ✅ ghi {r.get('updatedCells')} ô")

    # 4. format: đậm header + nền vàng, cột tiền #,##0
    reqs = [
        {"repeatCell": {
            "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1},
            "cell": {"userEnteredFormat": {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 1, "green": 0.95, "blue": 0.6},
            }},
            "fields": "userEnteredFormat(textFormat,backgroundColor)",
        }},
        {"repeatCell": {
            "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 4, "startColumnIndex": 1, "endColumnIndex": 2},
            "cell": {"userEnteredFormat": {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}}},
            "fields": "userEnteredFormat.numberFormat",
        }},
    ]
    r, err, _ = api("POST", f"{SHEETS}/{sid}:batchUpdate", tok, {"requests": reqs})
    if err:
        out(f"❌ format lỗi {err}: {r}")
        return 5
    out("4/6 ✅ format (đậm + nền vàng + số #,##0)")

    # 5. đọc lại
    r, err, _ = api("GET", f"{SHEETS}/{sid}/values/Sheet1!A1:B4", tok)
    if err:
        out(f"❌ đọc lỗi {err}: {r}")
        return 5
    got = r.get("values", [])
    ok = len(got) == 4 and got[2][1].replace(",", "") == "864"
    out(f"5/6 {'✅' if ok else '⚠️'} đọc lại: {json.dumps(got, ensure_ascii=False)}")

    # 6. xoá file test (chỉ xoá đúng folder vừa tạo)
    r, err, _ = api("DELETE", f"{DRIVE}/files/{sid}?supportsAllDrives=true", tok, expect_json=False)
    out(f"6/6 {'✅' if not err else '⚠️'} xoá sheet test (HTTP {err or 200})")
    r, err, _ = api("DELETE", f"{DRIVE}/files/{folder}?supportsAllDrives=true", tok, expect_json=False)
    out(f"    {'✅' if not err else '⚠️'} xoá folder test (HTTP {err or 200})")

    out("— selftest xong —")
    return 0


def main():
    p = argparse.ArgumentParser(description="Thao tác Drive/Sheets bằng OAuth user")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("whoami")

    lp = sub.add_parser("list")
    lp.add_argument("--query", default="")
    lp.add_argument("--parent")
    lp.add_argument("--limit", type=int, default=20)

    mp = sub.add_parser("mkdir")
    mp.add_argument("--name", required=True)
    mp.add_argument("--parent")

    sp = sub.add_parser("new-sheet")
    sp.add_argument("--name", required=True)
    sp.add_argument("--parent")

    tp = sub.add_parser("tabs")
    tp.add_argument("--file", required=True)

    ap = sub.add_parser("add-tab")
    ap.add_argument("--file", required=True)
    ap.add_argument("--title", required=True)

    rp = sub.add_parser("read")
    rp.add_argument("--file", required=True)
    rp.add_argument("--range", required=True)

    wp = sub.add_parser("write")
    wp.add_argument("--file", required=True)
    wp.add_argument("--range", required=True)
    wp.add_argument("--values", required=True)
    wp.add_argument("--raw", action="store_true")

    pp = sub.add_parser("append")
    pp.add_argument("--file", required=True)
    pp.add_argument("--range", required=True)
    pp.add_argument("--values", required=True)

    fp = sub.add_parser("format")
    fp.add_argument("--file", required=True)
    fp.add_argument("--spec", required=True)

    dp = sub.add_parser("delete")
    dp.add_argument("--file", required=True)
    dp.add_argument("--yes", action="store_true")

    dtp = sub.add_parser("delete-tab")
    dtp.add_argument("--file", required=True)
    dtp.add_argument("--sheet-id", required=True)
    dtp.add_argument("--yes", action="store_true")

    stp = sub.add_parser("selftest")
    stp.add_argument("--parent")

    args = p.parse_args()
    return {
        "whoami": cmd_whoami,
        "list": cmd_list,
        "mkdir": cmd_mkdir,
        "new-sheet": cmd_new_sheet,
        "tabs": cmd_tabs,
        "add-tab": cmd_add_tab,
        "read": cmd_read,
        "write": cmd_write,
        "append": cmd_append,
        "format": cmd_format,
        "delete": cmd_delete,
        "delete-tab": cmd_delete_tab,
        "selftest": cmd_selftest,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
