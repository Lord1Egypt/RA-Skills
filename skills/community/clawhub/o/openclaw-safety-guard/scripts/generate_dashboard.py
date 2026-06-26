#!/usr/bin/env python3
"""
Generates dashboard.html by:
1. Reading latest_status.json
2. Fetching Feishu bot info (name + avatar) for identity display
3. Running `vite build` on the React frontend (Figma Make design)
4. Injecting watchdog data into the single-file HTML output
"""
import os
import json
import subprocess
import sys
import shutil
import urllib.request
from utils import get_data_dir

FRONTEND_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "frontend"
)


def ensure_frontend_deps():
    """Install frontend dependencies if vite is not available yet."""
    vite_bin = os.path.join(FRONTEND_DIR, "node_modules", ".bin", "vite")
    if os.path.exists(vite_bin):
        return

    npm_bin = shutil.which("npm")
    if not npm_bin:
        print("Frontend deps missing and npm is not installed.", file=sys.stderr)
        print("Please install npm, then run setup.py or npm install in frontend/.", file=sys.stderr)
        sys.exit(1)

    print("Frontend deps missing, running npm install...")
    result = subprocess.run(
        [npm_bin, "install"],
        cwd=FRONTEND_DIR,
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        print(f"npm install failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)


def fetch_bot_info() -> dict:
    """Fetch Feishu bot name and avatar URL using app credentials.
    Returns empty dict if credentials are missing or call fails."""
    app_id = os.environ.get("FEISHU_APP_ID", "")
    app_secret = os.environ.get("FEISHU_APP_SECRET", "")
    if not app_id or not app_secret:
        print("WARN: FEISHU_APP_ID/SECRET not set, skipping bot info fetch")
        return {}
    try:
        # Step 1: get tenant access token
        token_payload = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
        req = urllib.request.Request(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            data=token_payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            token_data = json.loads(resp.read())
        token = token_data.get("tenant_access_token", "")
        if not token:
            print(f"WARN: Failed to get tenant token: {token_data}")
            return {}

        # Step 2: get bot info
        req = urllib.request.Request(
            "https://open.feishu.cn/open-apis/bot/v3/info",
            headers={"Authorization": f"Bearer {token}"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            bot_data = json.loads(resp.read())
        bot = bot_data.get("bot", {})
        return {
            "bot_name": bot.get("app_name", ""),
            "avatar_url": bot.get("avatar_url", ""),
        }
    except Exception as e:
        print(f"WARN: fetch_bot_info failed: {e}")
        return {}


def load_status():
    data_dir = get_data_dir()
    path = os.path.join(data_dir, "latest_status.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_frontend():
    """Run vite build to produce a single HTML file."""
    ensure_frontend_deps()
    dist_dir = os.path.join(FRONTEND_DIR, "dist")
    npm_bin = shutil.which("npm")
    if not npm_bin:
        print("npm is required to build the dashboard frontend.", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run(
        [npm_bin, "exec", "--", "vite", "build"],
        cwd=FRONTEND_DIR,
        capture_output=True,
        text=True,
        timeout=180,
    )
    if result.returncode != 0:
        print(f"Vite build failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    html_path = os.path.join(dist_dir, "index.html")
    if not os.path.exists(html_path):
        print(f"Build output not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()


def inject_data(html: str, data: dict) -> str:
    """Inject watchdog data and fix file:// compatibility."""
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    script_tag = f'<script>window.__WATCHDOG_DATA__={data_json};</script>'

    # crossorigin breaks file:// protocol (CORS), but type="module" is required for ES6
    html = html.replace(' crossorigin', '')

    if "</head>" in html:
        return html.replace("</head>", f"{script_tag}\n</head>", 1)
    return script_tag + "\n" + html


def main():
    print("Loading latest_status.json...")
    data = load_status()

    print("Fetching Feishu bot info...")
    bot_info = fetch_bot_info()
    if bot_info:
        data["bot_info"] = bot_info
        print(f"  Bot: {bot_info.get('bot_name', '?')} (avatar: {'yes' if bot_info.get('avatar_url') else 'no'})")
    else:
        data["bot_info"] = {}

    print("Building frontend (vite build --singlefile)...")
    html = build_frontend()

    print("Injecting watchdog data...")
    html = inject_data(html, data)

    data_dir = get_data_dir()
    out_path = os.path.join(data_dir, "dashboard.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"Dashboard generated: {out_path} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
