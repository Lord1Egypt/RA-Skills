#!/usr/bin/env python3
"""
Outlook OAuth2 — Browser-based Login (PKCE flow with local redirect)

Opens the Microsoft login page in your default browser.
Starts a local HTTP server on port 1456 to receive the OAuth callback.
Requires http://localhost:1456 registered as Web redirect URI in Azure app.

Usage:
    python3 oauth_web.py <account-id>
"""

import base64
import hashlib
import http.server
import json
import os
import random
import string
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data_dir import ACCOUNTS_DIR
REDIRECT_PORT = 1456
REDIRECT_URI = f"http://localhost:{REDIRECT_PORT}"


# ── PKCE  ────────────────────────────────────────────────────────────────


def _generate_code_verifier(length=64):
    chars = string.ascii_letters + string.digits + "-._~"
    return "".join(random.choice(chars) for _ in range(length))


def _generate_code_challenge(verifier):
    sha256 = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(sha256).rstrip(b"=").decode("ascii")


def _generate_state(length=32):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def _open_browser(url):
    """Open URL in default browser (cross-platform)."""
    import platform as _plt
    system = _plt.system()
    try:
        if system == "Windows":
            os.system(f'start "" "{url}"')
        elif system == "Darwin":
            subprocess.Popen(["open", url])
        else:  # Linux and other Unix-like
            subprocess.Popen(["xdg-open", url])
        return True
    except Exception:
        return False


# ── OAuth Server ──────────────────────────────────────────────────────────


_oauth_code = None
_oauth_error = None
_expected_state = None
_server_shutdown = threading.Event()


class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global _oauth_code, _oauth_error, _expected_state
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/favicon.ico":
            self._respond(200, "OK")
            return

        code = params.get("code", [None])[0]
        state = params.get("state", [None])[0]
        error = params.get("error", [None])[0]
        error_desc = params.get("error_description", [None])[0]

        # ⚠️ SECURITY: Verify OAuth state to prevent CSRF attack
        if state != _expected_state:
            _oauth_error = "state_mismatch: OAuth state parameter does not match. Possible CSRF attack, authorization rejected."
            self._respond_html(400, "<h2>❌ 安全校验失败</h2><p>OAuth state 不匹配，请求已拒绝。</p>")
            _server_shutdown.set()
            return

        if error:
            _oauth_error = f"{error}: {error_desc}"
            self._respond_html(400, f"<h2>❌ 授权失败</h2><p>{error}</p><p>{error_desc}</p>")
        elif code:
            _oauth_code = code
            self._respond_html(200, "<h2>✅ 授权成功！</h2><p>你可以关闭此页面了。</p><script>window.close()</script>")
        else:
            self._respond_html(400, "<h2>❌ 无效请求</h2><p>未收到授权码。</p>")

        _server_shutdown.set()

    def _respond(self, status, body, content_type="text/plain"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def _respond_html(self, status, html):
        full = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>Email Assistant - OAuth</title>
<style>body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#f5f5f5;}}
.card{{background:white;padding:48px;border-radius:16px;box-shadow:0 2px 16px rgba(0,0,0,0.1);text-align:center;}}
h2{{margin-top:0;}}</style></head><body><div class="card">{html}</div></body></html>"""
        self._respond(status, full, "text/html; charset=utf-8")

    def log_message(self, format, *args):
        pass


def _start_server():
    server = http.server.HTTPServer(("127.0.0.1", REDIRECT_PORT), OAuthHandler)
    server.timeout = 1.0

    def serve():
        while not _server_shutdown.is_set():
            server.handle_request()

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    return thread


# ── Token Exchange ─────────────────────────────────────────────────────────


def _exchange_code(client_id, tenant_id, code, code_verifier):
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "client_id": client_id, "grant_type": "authorization_code",
        "code": code, "redirect_uri": REDIRECT_URI, "code_verifier": code_verifier,
    }
    payload = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(token_url, data=payload, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if "access_token" in result:
                result["stored_at"] = time.time()
                return result
            else:
                print(f"[ERROR] 令牌响应异常: {result}", file=sys.stderr)
                return None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"[ERROR] 令牌交换失败 HTTP {e.code}: {body}", file=sys.stderr)
        return None


# ── Main Flow ──────────────────────────────────────────────────────────────


def run_oauth_flow(account_id):
    global _oauth_code, _oauth_error, _expected_state
    _oauth_code = None
    _oauth_error = None
    _expected_state = None
    _server_shutdown.clear()

    acct_path = os.path.join(ACCOUNTS_DIR, f"{account_id}.json")
    if not os.path.exists(acct_path):
        print(f"[ERROR] 账户配置不存在: {acct_path}", file=sys.stderr)
        sys.exit(1)

    with open(acct_path, "r", encoding="utf-8") as f:
        account = json.load(f)

    if account.get("type") != "outlook":
        print(f"[ERROR] '{account_id}' 不是 Outlook 账户。", file=sys.stderr)
        sys.exit(1)

    oauth = account.get("oauth", {})
    client_id = oauth.get("client_id")
    tenant_id = oauth.get("tenant_id", "consumers")
    if not client_id:
        print("[ERROR] 缺少 oauth.client_id。", file=sys.stderr)
        sys.exit(1)

    scopes = oauth.get("scopes", ["User.Read", "Mail.ReadWrite", "Mail.Send"])
    code_verifier = _generate_code_verifier()
    code_challenge = _generate_code_challenge(code_verifier)
    state = _generate_state()
    # ⚠️ SECURITY: Save expected state for CSRF verification in callback handler
    _expected_state = state
    scope_str = " ".join(scopes)

    authorize_url = (
        f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
        f"?client_id={urllib.parse.quote(client_id, safe='')}"
        f"&response_type=code"
        f"&redirect_uri={urllib.parse.quote(REDIRECT_URI, safe='')}"
        f"&scope={urllib.parse.quote(scope_str, safe='')}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
        f"&state={state}"
        f"&prompt=select_account"
    )

    print("[INFO] 启动本地回调服务器...")
    _start_server()

    print("[INFO] 正在打开浏览器进行 Microsoft 授权...")
    if _open_browser(authorize_url):
        print("  ✅ 浏览器已打开！请在浏览器中登录你的 Microsoft 账户。")
    else:
        print("  ⚠️  无法自动打开浏览器，请手动访问：")
        print(f"  {authorize_url}")
    print()
    print(f"  ⏳ 等待授权完成（回调地址: {REDIRECT_URI}）...")

    timeout = 300
    start = time.time()
    while _oauth_code is None and _oauth_error is None:
        if time.time() - start > timeout:
            print(f"\n[ERROR] 授权超时（{timeout} 秒）。")
            _server_shutdown.set()
            sys.exit(1)
        time.sleep(0.5)

    _server_shutdown.set()

    if _oauth_error:
        print(f"\n[ERROR] 授权失败: {_oauth_error}", file=sys.stderr)
        sys.exit(1)

    print("\n[INFO] 收到授权码，正在交换令牌...")
    token = _exchange_code(client_id, tenant_id, _oauth_code, code_verifier)
    if not token:
        sys.exit(1)

    token_path = os.path.join(ACCOUNTS_DIR, f"{account_id}.token.json")
    with open(token_path, "w", encoding="utf-8") as f:
        json.dump(token, f, indent=2, ensure_ascii=False)

    # Update user email from JWT
    access_token = token.get("access_token", "")
    if access_token and account.get("user") in ("", None, "user@outlook.com"):
        try:
            parts = access_token.split(".")
            if len(parts) == 3:
                payload = parts[1]
                padding = 4 - len(payload) % 4
                if padding != 4:
                    payload += "=" * padding
                claims = json.loads(base64.urlsafe_b64decode(payload))
                email = claims.get("email") or claims.get("preferred_username")
                if email:
                    account["user"] = email
                    with open(acct_path, "w", encoding="utf-8") as f:
                        json.dump(account, f, indent=2, ensure_ascii=False)
                    print(f"[INFO] 邮箱地址已更新: {email}")
        except Exception:
            pass

    print(f"\n✅ OAuth 授权完成！")
    print(f"   账户: {account.get('user', account_id)}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 oauth_web.py <account-id>")
        sys.exit(1)
    run_oauth_flow(sys.argv[1])


if __name__ == "__main__":
    main()
