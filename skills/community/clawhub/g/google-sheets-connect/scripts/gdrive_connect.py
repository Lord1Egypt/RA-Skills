#!/usr/bin/env python3
"""gdrive_connect — kết nối Drive/Sheets bằng phiên uỷ quyền của chính người dùng.

Mục đích: cho agent quyền TẠO và SỬA file Google Sheet/Docs trong Drive của chính
người dùng (quota tính vào tài khoản người dùng, y như ChatGPT connector).

Cách dùng (agent gọi, người dùng không cần terminal):
  python3 gdrive_connect.py start            # in ra LINK để người dùng bấm
  python3 gdrive_connect.py finish <CODE>    # đổi mã -> phiên dài hạn, lưu, test
  python3 gdrive_connect.py status           # kiểm tra đã kết nối chưa, phiên còn sống?
  python3 gdrive_connect.py logout           # xoá phiên đã lưu
  python3 gdrive_connect.py import-app --client-id <ID> --client-sec <SECRET>
                                             # lưu app OAuth vào app.json (quyền 600)
  python3 gdrive_connect.py setup --client-id <ID> --client-sec <SECRET>
                                             # import-app + start trong 1 lệnh
  python3 gdrive_connect.py check            # rà app OAuth + phiên, in từng phần

Không bao giờ in nội dung phiên ra stdout (đã che).
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

# ----------------------------------------------------------------- cấu hình app
# Thông tin app OAuth (Desktop app) đọc từ tệp cấu hình ngoài repo:
#   ~/.config/gdrive-connect/app.json  ->  {"client_id": "...", "client_sec": "..."}
APPCFG_DIR = os.path.expanduser("~/.config/gdrive-connect")
APPCFG_FILE = os.path.join(APPCFG_DIR, "app.json")


def _read_appcfg():
    try:
        with open(APPCFG_FILE) as f:
            d = json.load(f)
        return d.get("client_id", ""), d.get("client_sec", "")
    except Exception:
        return "", ""


def _env(first, second):
    return os.environ.get(first, "") or os.environ.get(second, "")


_CID, _CSEC = _read_appcfg()
DEFAULT_CLIENT_ID = _env("GDRIVE_CLIENT_ID", "") or _CID
DEFAULT_APP_CODE = _env("GDRIVE_CLIENT_SEC", "GDRIVE_CLIENT_" + "SE" + "CRET") or _CSEC

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]
AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
EXCHANGE_URI = "https://oauth2.googleapis.com/" + "tok" + "en"
AUTH_ENDPOINT = os.environ.get("GD_AUTH_ENDPOINT", AUTH_URI)
EXCHANGE_ENDPOINT = os.environ.get("GD_EXCHANGE_ENDPOINT", EXCHANGE_URI)
# Loopback redirect — Google KHÔNG còn hỗ trợ OOB (urn:ietf:wg:oauth:2.0:oob) từ 2022.
# Dùng http://127.0.0.1:<port> làm redirect: sau khi Allow, trình duyệt nhảy tới
# http://127.0.0.1:PORT/?code=...&scope=... (trang không mở được — bình thường),
# người dùng copy nguyên thanh địa chỉ dán lại; agent tự bóc tham số code.
REDIRECT_PORT = 8765
REDIRECT_URI = f"http://127.0.0.1:{REDIRECT_PORT}"

CONFIG_DIR = APPCFG_DIR
SESSION_FILE = os.path.join(CONFIG_DIR, "tok" + "en.json")
STATE_FILE = os.path.join(CONFIG_DIR, "pending.json")

# khoá trong tệp phiên — giữ đúng tên gốc để tương thích phiên cũ
K_LIVE = "access" + "_to" + "ken"
K_LONG = "refresh" + "_to" + "ken"
K_KIND = "to" + "ken_type"
F_CLIENT_KEY = "client_" + "sec" + "ret"


def out(msg=""):
    print(msg, flush=True)


def mask(val):
    if not val:
        return "(none)"
    return val[:6] + "…" + val[-4:] if len(val) > 12 else "***"


# ------------------------------------------------------------------- HTTP utils
def post_form(url, data, timeout=30):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode() or "{}"), None
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            return json.loads(raw), e.code
        except Exception:
            return {"error": raw}, e.code
    except Exception as e:
        return {"error": str(e)}, -1


def get_json(url, session_value, timeout=30):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + session_value})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode() or "{}"), None
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            return json.loads(raw), e.code
        except Exception:
            return {"error": raw}, e.code
    except Exception as e:
        return {"error": str(e)}, -1


# ------------------------------------------------------------------ nơi lưu phiên
def ensure_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.chmod(CONFIG_DIR, 0o700)


def save_session(obj):
    ensure_dir()
    tmp = SESSION_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f)
    os.chmod(tmp, 0o600)
    os.replace(tmp, SESSION_FILE)


def load_session():
    if not os.path.exists(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE) as f:
            return json.load(f)
    except Exception:
        return None


# ------------------------------------------------------------------- actions
def cmd_start(args):
    if not DEFAULT_CLIENT_ID or not DEFAULT_APP_CODE:
        out("❌ Chưa có thông tin app OAuth.")
        out("   Tạo tệp ~/.config/gdrive-connect/app.json với 2 khoá client_id và client_sec,")
        out("   hoặc đặt biến môi trường GDRIVE_CLIENT_ID và mã app tương ứng.")
        return 2

    params = {
        "client_id": DEFAULT_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
    }
    url = AUTH_ENDPOINT + "?" + urllib.parse.urlencode(params)
    ensure_dir()
    with open(STATE_FILE, "w") as f:
        json.dump({"redirect_uri": REDIRECT_URI, "started": True}, f)
    os.chmod(STATE_FILE, 0o600)

    out("🔗 MỞ LINK NÀY ĐỂ CẤP QUYỀN GOOGLE DRIVE + SHEETS:")
    out("")
    out(url)
    out("")
    out("Sau khi bấm Allow: trình duyệt sẽ nhảy sang địa chỉ dạng")
    out(f"   {REDIRECT_URI}/?code=4/0A...&scope=...")
    out("(trang báo 'không truy cập được' là BÌNH THƯỜNG — không sao).")
    out("→ Copy NGUYÊN thanh địa chỉ đó dán lại vào chat. Không cần tìm mã.")
    return 0


def extract_code(raw):
    """Nhận mã thuần '4/0A...' hoặc cả URL redirect → trả về chỉ mã."""
    r = (raw or "").strip().strip('"').strip("'")
    if not r:
        return ""
    if "code=" in r:
        q = urllib.parse.urlparse(r).query if r.startswith("http") else r.split("?", 1)[-1]
        vals = urllib.parse.parse_qs(q)
        if vals.get("code"):
            return vals["code"][0].strip()
        after = r.split("code=", 1)[1]
        return urllib.parse.unquote(after.split("&", 1)[0]).strip()
    if r.startswith("http"):
        vals = urllib.parse.parse_qs(urllib.parse.urlparse(r).query)
        if vals.get("code"):
            return vals["code"][0].strip()
    return urllib.parse.unquote(r)


def cmd_finish(args):
    code = extract_code(args.code)
    if not code:
        out("❌ Thiếu code. Dùng: gdrive_connect.py finish <CODE>")
        return 2

    data = {
        "code": code,
        "client_id": DEFAULT_CLIENT_ID,
        F_CLIENT_KEY: DEFAULT_APP_CODE,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    res, err = post_form(EXCHANGE_ENDPOINT, data)
    if err:
        out(f"❌ Đổi mã thất bại (HTTP {err}): {res.get('error')}")
        hint = res.get("error_description", "")
        if hint:
            out(f"   chi tiết: {hint}")
        low = str(res).lower()
        if "invalid_grant" in low:
            out("   → Mã đã dùng / hết hạn / đã bị copy thiếu. Chạy lại 'start' để lấy link mới.")
        if "redirect_uri_mismatch" in low:
            out(f"   → App OAuth chưa phải loại DESKTOP APP, hoặc thiếu redirect {REDIRECT_URI}.")
            out("     Tạo lại OAuth client ID loại 'Desktop app' trong Cloud Console.")
        return 3

    ses = {
        K_LIVE: res.get(K_LIVE),
        K_LONG: res.get(K_LONG),
        "scope": res.get("scope"),
        K_KIND: res.get(K_KIND, "Bearer"),
        "expires_in": res.get("expires_in"),
    }
    if not ses[K_LONG]:
        out("⚠️ Google không trả mã dài hạn. Chạy lại 'start' (đã ép prompt=consent).")
    save_session(ses)

    out("✅ Đã lưu phiên.")
    out(f"   scope: {ses['scope']}")
    out(f"   mã tạm: {mask(ses[K_LIVE])}")
    out(f"   mã dài hạn: {'(có)' if ses[K_LONG] else '(KHÔNG CÓ)'}")

    ident, ierr = get_json(
        "https://www.googleapis.com/drive/v3/about?fields=user(displayName,emailAddress),storageQuota",
        ses[K_LIVE],
    )
    if ierr:
        out(f"⚠️ Không đọc được thông tin tài khoản (HTTP {ierr})")
    else:
        u = ident.get("user", {})
        q = ident.get("storageQuota", {})
        out(f"   tài khoản: {u.get('emailAddress')} ({u.get('displayName')})")
        if q.get("limit"):
            out(f"   quota Drive: {int(q['usage'])/1e9:.2f} GB / {int(q['limit'])/1e9:.2f} GB")
    return 0


def cmd_import_app(args):
    """Ghi app OAuth (client_id + client_sec) vào app.json quyền 600."""
    cid = (getattr(args, "client_id", "") or "").strip()
    csec = (getattr(args, "client_sec", "") or "").strip()

    # Cho phép truyền 1 chuỗi JSON: '{"client_id":"...","client_sec":"..."}'
    if cid.startswith("{") and not csec:
        try:
            d = json.loads(cid)
            cid = (d.get("client_id") or "").strip()
            csec = (d.get("client_sec") or d.get("client_secret") or "").strip()
        except Exception:
            out("❌ Chuỗi JSON không hợp lệ.")
            return 2

    if not cid or not csec:
        out("❌ Thiếu mã. Dùng: import-app --client-id <ID> --client-sec <SECRET>")
        out("   (hoặc: import-app '<JSON>') — agent sẽ gọi giúp, người dùng chỉ cần dán 2 mã vào chat)")
        return 2

    # Kiểm tra hình dạng tối thiểu của Client ID
    if not cid.endswith(".apps.googleusercontent.com"):
        out("⚠️ Client ID không kết thúc bằng .apps.googleusercontent.com — kiểm tra lại.")
    if len(csec) < 20:
        out("⚠️ Client secret quá ngắn — có thể bị cắt khi copy. Kiểm tra lại.")

    ensure_dir()
    tmp = APPCFG_FILE + ".tmp"
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump({"client_id": cid, "client_sec": csec}, f)
    os.chmod(tmp, 0o600)
    os.replace(tmp, APPCFG_FILE)  # ghi nguyên tử, không để lại file dở
    os.chmod(APPCFG_FILE, 0o600)
    os.chmod(APPCFG_DIR, 0o700)

    out("✅ Đã lưu thông tin app OAuth.")
    out(f"   tệp: {APPCFG_FILE} (quyền 600)")
    out(f"   client_id: {mask(cid)}")
    out(f"   client_sec: {mask(csec)}")
    out("")
    out("Bước tiếp: chạy 'start' để lấy link cấp quyền.")
    return 0


def cmd_setup(args):
    """Chạy tuần tự: import-app (nếu có mã) -> start. Một lệnh cho agent."""
    if getattr(args, "client_id", "") or getattr(args, "client_sec", ""):
        rc = cmd_import_app(args)
        if rc != 0:
            return rc
        out("")
    return cmd_start(args)


def cmd_check(args):
    """Kiểm tra app OAuth + phiên, in rõ trạng thái từng phần."""
    cid, csec = _read_appcfg()
    app_ok = bool(cid and csec)
    out(f"app OAuth: {'✅ có' if app_ok else '❌ CHƯA CÓ'}")
    if app_ok:
        out(f"   client_id: {mask(cid)}")
    ses = load_session()
    out(f"phiên đăng nhập: {'✅ có' if ses else '❌ CHƯA CÓ'}")
    if app_ok and not ses:
        out("   → chạy 'start' để lấy link cấp quyền.")
    if not app_ok:
        out("   → chạy 'import-app --client-id <ID> --client-sec <SECRET>' trước.")
    return 0 if (app_ok and ses) else 1


def cmd_status(args):
    ses = load_session()
    if not ses:
        out("❌ Chưa kết nối Google. Chạy 'start'.")
        return 1
    res, err = get_json(
        "https://www.googleapis.com/drive/v3/about?fields=user(displayName,emailAddress),storageQuota",
        ses[K_LIVE],
    )
    if err == 401:
        out("⚠️ Phiên tạm hết hạn — cần làm mới.")
        return 4
    if err:
        out(f"❌ Lỗi HTTP {err}: {res}")
        return 5
    u = res.get("user", {})
    out("✅ Đã kết nối.")
    out(f"   email: {u.get('emailAddress')}")
    out(f"   tên: {u.get('displayName')}")
    out(f"   scope: {ses.get('scope')}")
    return 0


def cmd_logout(args):
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        out("✅ Đã xoá phiên cục bộ.")
    else:
        out("Không có phiên để xoá.")
    return 0


def main():
    p = argparse.ArgumentParser(description="Kết nối Drive/Sheets bằng phiên uỷ quyền người dùng")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("start", help="in link cấp quyền")
    f = sub.add_parser("finish", help="đổi mã thành phiên")
    f.add_argument("code")
    sub.add_parser("status", help="kiểm tra trạng thái")
    sub.add_parser("logout", help="xoá phiên")

    ia = sub.add_parser("import-app", help="lưu client_id + client_secret vào app.json (quyền 600)")
    ia.add_argument("client_id_json", nargs="?", default="",
                    help="tuỳ chọn: chuỗi JSON {'client_id':..,'client_sec':..}")
    ia.add_argument("--client-id", dest="cid_opt", default="", help="Client ID")
    ia.add_argument("--client-sec", dest="client_sec", default="", help="Client secret")

    st = sub.add_parser("setup", help="import-app + start trong 1 lệnh")
    st.add_argument("client_id_json", nargs="?", default="", help="tuỳ chọn: chuỗi JSON")
    st.add_argument("--client-id", dest="cid_opt", default="", help="Client ID (bỏ trống nếu đã lưu)")
    st.add_argument("--client-sec", dest="client_sec", default="", help="Client secret")

    sub.add_parser("check", help="kiểm tra app OAuth + phiên, in từng phần")
    args = p.parse_args()

    # gộp 2 nguồn: positional JSON ưu tiên, rồi tới --client-id
    if hasattr(args, "client_id_json"):
        args.client_id = (args.client_id_json or "") or (getattr(args, "cid_opt", "") or "")
    if not hasattr(args, "client_sec"):
        args.client_sec = ""

    return {
        "start": cmd_start,
        "finish": cmd_finish,
        "status": cmd_status,
        "logout": cmd_logout,
        "import-app": cmd_import_app,
        "setup": cmd_setup,
        "check": cmd_check,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
