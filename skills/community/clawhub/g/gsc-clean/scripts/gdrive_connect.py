#!/usr/bin/env python3
"""gdrive_connect — kết nối Drive/Sheets bằng phiên uỷ quyền của chính người dùng.

Mục đích: cho agent quyền TẠO và SỬA file Google Sheet/Docs trong Drive của chính
người dùng (quota tính vào tài khoản người dùng, y như ChatGPT connector).

Chỉ dùng thư viện chuẩn Python 3 + google-auth/google-api-python-client (nếu có).

Cách dùng (agent gọi, người dùng không cần terminal):
  python3 gdrive_connect.py start            # in ra LINK để người dùng bấm
  python3 gdrive_connect.py finish <CODE>    # đổi code -> refresh token, lưu, test
  python3 gdrive_connect.py status           # kiểm tra đã kết nối chưa, token còn sống?
  python3 gdrive_connect.py logout           # xoá token đã lưu

KHÔNG in token ra stdout (đã mask).
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

# ----------------------------------------------------------------- OAuth config
# Lấy thông tin app OAuth (Desktop app) từ tệp cấu hình ngoài repo.
APPCFG_FILE = os.path.expanduser("~/.config/gdrive-connect/app.json")


def _load_appcfg():
    try:
        with open(APPCFG_FILE) as f:
            d = json.load(f)
        return d.get("client_id", ""), d.get("client_sec", "")
    except Exception:
        return "", ""


_CID, _CSEC = _load_appcfg()
DEFAULT_CLIENT_ID = os.environ.get("GDRIVE_CLIENT_ID", "") or _CID
DEFAULT_CLIENT_SECRET = os.environ.get("GDRIVE_CLIENT_SECRET", "") or _CSEC

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]
AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"
# OOB (out-of-band) flow: Google trả code để user dán lại. Google đã deprecate OOB
# cho một số client; nếu bị chặn, script báo lỗi và hướng dẫn dùng loopback.
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"

CONFIG_DIR = os.path.expanduser("~/.config/gdrive-connect")
TOKEN_FILE = os.path.join(CONFIG_DIR, "token.json")
STATE_FILE = os.path.join(CONFIG_DIR, "pending.json")


def out(msg=""):
    print(msg, flush=True)


def mask(tok):
    if not tok:
        return "(none)"
    return tok[:6] + "…" + tok[-4:] if len(tok) > 12 else "***"


# ------------------------------------------------------------------- HTTP utils
def http_post_form(url, data, timeout=30):
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


def http_get_json(url, token, timeout=30):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
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


# ------------------------------------------------------------------ token store
def ensure_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.chmod(CONFIG_DIR, 0o700)


def save_token(obj):
    ensure_dir()
    tmp = TOKEN_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f)
    os.chmod(tmp, 0o600)
    os.replace(tmp, TOKEN_FILE)


def load_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    try:
        with open(TOKEN_FILE) as f:
            return json.load(f)
    except Exception:
        return None


# ------------------------------------------------------------------- actions
def cmd_start(args):
    if not DEFAULT_CLIENT_ID or not DEFAULT_CLIENT_SECRET:
        out("❌ Chưa có thông tin app OAuth.")
        out("   Đặt env GDRIVE_CLIENT_ID / GDRIVE_CLIENT_SECRET, hoặc tạo ~/.config/gdrive-connect/app.json (client_id, client_sec).")
        return 2

    params = {
        "client_id": DEFAULT_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
    }
    url = AUTH_URI + "?" + urllib.parse.urlencode(params)
    ensure_dir()
    with open(STATE_FILE, "w") as f:
        json.dump({"redirect_uri": REDIRECT_URI, "started": True}, f)
    os.chmod(STATE_FILE, 0o600)

    out("🔗 MỞ LINK NÀY ĐỂ CẤP QUYỀN GOOGLE DRIVE + SHEETS:")
    out("")
    out(url)
    out("")
    out("Sau khi bấm Allow, Google hiện 1 mã code → copy và dán lại vào chat.")
    return 0


def cmd_finish(args):
    code = (args.code or "").strip()
    if not code:
        out("❌ Thiếu code. Dùng: gdrive_connect.py finish <CODE>")
        return 2

    data = {
        "code": code,
        "client_id": DEFAULT_CLIENT_ID,
        "client_secret": DEFAULT_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    res, err = http_post_form(TOKEN_URI, data)
    if err:
        out(f"❌ Đổi code thất bại (HTTP {err}): {res.get('error')}")
        hint = res.get("error_description", "")
        if hint:
            out(f"   chi tiết: {hint}")
        if "invalid_grant" in str(res).lower():
            out("   → Code đã dùng hoặc hết hạn. Chạy lại 'start' để lấy link mới.")
        return 3

    tok = {
        "access_token": res.get("access_token"),
        "refresh_token": res.get("refresh_token"),
        "scope": res.get("scope"),
        "token_type": res.get("token_type", "Bearer"),
        "expires_in": res.get("expires_in"),
    }
    if not tok["refresh_token"]:
        out("⚠️ Google không trả refresh_token. Chạy lại 'start' (đã ép prompt=consent).")
    save_token(tok)

    out("✅ Đã lưu token.")
    out(f"   scope: {tok['scope']}")
    out(f"   access_token: {mask(tok['access_token'])}")
    out(f"   refresh_token: {'(có)' if tok['refresh_token'] else '(KHÔNG CÓ)'}")

    ident, ierr = http_get_json(
        "https://www.googleapis.com/drive/v3/about?fields=user(displayName,emailAddress),storageQuota",
        tok["access_token"],
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


def cmd_status(args):
    tok = load_token()
    if not tok:
        out("❌ Chưa kết nối Google. Chạy 'start'.")
        return 1
    res, err = http_get_json(
        "https://www.googleapis.com/drive/v3/about?fields=user(displayName,emailAddress),storageQuota",
        tok["access_token"],
    )
    if err == 401:
        out("⚠️ access_token hết hạn — cần refresh.")
        return 4
    if err:
        out(f"❌ Lỗi HTTP {err}: {res}")
        return 5
    u = res.get("user", {})
    out("✅ Đã kết nối.")
    out(f"   email: {u.get('emailAddress')}")
    out(f"   tên: {u.get('displayName')}")
    out(f"   scope: {tok.get('scope')}")
    return 0


def cmd_logout(args):
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        out("✅ Đã xoá token cục bộ.")
    else:
        out("Không có token để xoá.")
    return 0


def main():
    p = argparse.ArgumentParser(description="Kết nối Google Drive/Sheets bằng OAuth user")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("start", help="in link cấp quyền")
    f = sub.add_parser("finish", help="đổi code thành token")
    f.add_argument("code")
    sub.add_parser("status", help="kiểm tra trạng thái")
    sub.add_parser("logout", help="xoá token")
    args = p.parse_args()

    return {
        "start": cmd_start,
        "finish": cmd_finish,
        "status": cmd_status,
        "logout": cmd_logout,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
