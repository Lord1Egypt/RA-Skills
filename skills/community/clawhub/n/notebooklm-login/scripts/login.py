#!/usr/bin/env python3
"""NotebookLM MCP login - launch Chrome, extract cookies, save auth profile.

Usage:
  DISPLAY=:0 python3 login.py

The script will:
1. Launch Chromium with remote debugging on port 9222
2. Wait for the user to log in to Google in the browser window
3. Extract auth cookies via CDP
4. Save them to ~/.notebooklm-mcp-cli/profiles/default/

Requires: notebooklm-mcp-cli package (uv tool install notebooklm-mcp-cli)
"""
import subprocess, sys, os, time, httpx

# Locate the notebooklm-mcp-cli package
UV_TOOLS = os.path.expanduser("~/.local/share/uv/tools/notebooklm-mcp-cli/lib/python3.11/site-packages")
if os.path.isdir(UV_TOOLS):
    sys.path.insert(0, UV_TOOLS)

CHROME = "/usr/bin/chromium-browser"
PORT = 9222
TMP_PROFILE = "/tmp/nlm-chrome-profile"
LOGIN_TIMEOUT = 300  # seconds


def launch_chrome():
    os.makedirs(TMP_PROFILE, exist_ok=True)
    proc = subprocess.Popen(
        [CHROME, f"--remote-debugging-port={PORT}",
         "--no-first-run", "--no-default-browser-check",
         "--disable-extensions", f"--user-data-dir={TMP_PROFILE}",
         "--remote-allow-origins=*"],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )
    return proc


def wait_for_cdp(timeout=15):
    client = httpx.Client()
    for _ in range(timeout):
        try:
            r = client.get(f"http://localhost:{PORT}/json/version", timeout=3)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        time.sleep(1)
    return None


def main():
    print("Launching Chrome...")
    proc = launch_chrome()
    print(f"Chrome PID: {proc.pid}")

    print("Waiting for CDP...")
    info = wait_for_cdp()
    if not info:
        err = proc.stderr.read().decode()[:300] if proc.poll() is not None else "still running"
        print(f"ERROR: CDP not available. Chrome: {err}")
        sys.exit(1)
    print(f"CDP ready: {info.get('Browser')}")

    from notebooklm_tools.utils.cdp import extract_cookies_via_existing_cdp
    from notebooklm_tools.core.auth import get_auth_manager

    print(f"\n请在弹出的浏览器窗口中登录 Google 账号...")
    print(f"Waiting up to {LOGIN_TIMEOUT}s...\n")

    result = extract_cookies_via_existing_cdp(
        cdp_url=f"http://localhost:{PORT}",
        wait_for_login=True,
        login_timeout=LOGIN_TIMEOUT,
    )

    email = result.get("email", "N/A")
    cookies = result["cookies"]
    print(f"✅ Login successful! Email: {email}, Cookies: {len(cookies)}")

    mgr = get_auth_manager()
    mgr.save_profile(
        cookies=cookies,
        csrf_token=result.get("csrf_token", ""),
        session_id=result.get("session_id", ""),
        email=email,
        force=False,
        build_label=result.get("build_label", ""),
    )
    print("✅ Profile saved!")

    if mgr.profile_exists():
        p = mgr.load_profile()
        print(f"✅ Verified: {p.email}, {len(p.cookies)} cookies")
    else:
        print("⚠️ Verification failed")


if __name__ == "__main__":
    main()
