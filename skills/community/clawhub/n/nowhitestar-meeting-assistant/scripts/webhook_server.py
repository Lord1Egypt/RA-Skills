#!/usr/bin/env python3
# DEPRECATED: 此文件已合并到 run_calendar_services.py。
# 请使用 run_calendar_services.py 一站式启动 webhook + tunnel + watch。
# 保留此文件仅作参考。

"""
Google Calendar Push Notification webhook 服务器。

接收 Google Calendar 的推送通知 → 触发日历同步 → 更新 schedule.json → SIGHUP scheduler。

用法：
  webhook_server.py <port>
  webhook_server.py <port> --ngrok-url <url>   # 首次启动时注册 watch 频道
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "meeting-assistant"
STATE_PATH = CONFIG_DIR / ".watch_state.json"
LOG_PATH = CONFIG_DIR / "webhook.log"
SCRIPT_DIR = Path(__file__).resolve().parent

GOG_ACCOUNT = os.environ.get("GOG_ACCOUNT", "default")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
REFRESH_TOKEN = os.environ.get("GOG_REFRESH_TOKEN", "")

# Deprecated fallback server: keep defaults generic and load real calendar IDs
# from environment when needed. Prefer run_calendar_services.py.
CALENDARS = [
    {"id": os.environ.get("GOOGLE_CALENDAR_ID", "primary"), "label": "primary"},
]

LOCK = threading.Lock()
LAST_SYNC = 0
SYNC_COOLDOWN = 10  # 秒，防止通知风暴重复同步


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def _get_access_token():
    """用 refresh token 换取 access token。"""
    import urllib.parse
    import urllib.request

    if not (GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET and REFRESH_TOKEN):
        raise RuntimeError(
            "Missing Google OAuth environment variables: "
            "GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOG_REFRESH_TOKEN"
        )

    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
    }).encode()
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=data,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = json.loads(resp.read())
    return body["access_token"]


def do_sync():
    """执行日历同步：check_meetings → schedule.json → SIGHUP scheduler。"""
    global LAST_SYNC
    now = time.time()
    if now - LAST_SYNC < SYNC_COOLDOWN:
        log("⏭ 同步冷却中，跳过")
        return False
    LAST_SYNC = now

    try:
        # 运行 check_meetings.py 获取本周会议
        r = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "check_meetings.py"), "week", "--json"],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode != 0:
            log(f"⚠️ check_meetings 失败: {r.stderr}")
            return False

        meetings = json.loads(r.stdout)
        log(f"📅 获取到 {len(meetings)} 个会议")

        # 构建 schedule 事件
        events = []
        now_local = datetime.now()
        for m in meetings:
            try:
                start = datetime.fromisoformat(m["start"].replace("Z", "+00:00"))
                end = datetime.fromisoformat(m["end"].replace("Z", "+00:00"))
            except (ValueError, KeyError):
                continue

            # 跳过已过期和在录制中的
            if end < now_local:
                continue

            title = m["title"]
            meeting_id = m.get("id", str(uuid.uuid4()))

            # 提前 5 分钟提醒
            remind_at = start - timedelta(minutes=5)
            if remind_at > now_local:
                events.append({
                    "kind": "remind",
                    "at": remind_at.isoformat(),
                    "title": title,
                    "meeting_id": meeting_id,
                })

            # 开始时间弹录制
            if start > now_local:
                events.append({
                    "kind": "ask_record",
                    "at": start.isoformat(),
                    "title": title,
                    "meeting_id": meeting_id,
                })

        schedule = {"events": events, "meetings": meetings}
        SCHEDULE_PATH = CONFIG_DIR / "schedule.json"
        SCHEDULE_PATH.write_text(json.dumps(schedule, indent=2, ensure_ascii=False))
        log(f"✅ schedule.json 已更新，{len(events)} 个事件")

        # SIGHUP scheduler 重载
        try:
            r = subprocess.run(
                ["pgrep", "-f", "scheduler_daemon.py"],
                capture_output=True, text=True, timeout=5,
            )
            for pid in r.stdout.strip().splitlines():
                pid = pid.strip()
                if pid:
                    os.kill(int(pid), signal.SIGHUP)
                    log(f"📡 SIGHUP 已发送到 scheduler (pid={pid})")
        except Exception as e:
            log(f"⚠️ SIGHUP 失败: {e}")

        return True
    except Exception as e:
        log(f"❌ 同步异常: {e}")
        return False


def register_watch(ngrok_url):
    """为所有日历注册 Google Calendar push notification channel。"""
    from urllib.request import Request, urlopen
    import urllib.parse
    import urllib.error

    token = _get_access_token()
    channel_id = str(uuid.uuid4())

    results = []
    for cal in CALENDARS:
        cal_id = urllib.parse.quote(cal["id"], safe="")
        url = f"https://www.googleapis.com/calendar/v3/calendars/{cal_id}/events/watch"
        body = json.dumps({
            "id": channel_id,
            "type": "web_hook",
            "address": f"{ngrok_url.rstrip('/')}/calendar-webhook",
        }).encode()

        req = Request(
            url, data=body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
            # 7 天后过期
            expires = datetime.fromtimestamp(int(data["expiration"]) / 1000, tz=timezone.utc)
            results.append({
                "calendar_id": cal["id"],
                "label": cal["label"],
                "channel_id": channel_id,
                "resource_id": data.get("resourceId", ""),
                "expires": expires.isoformat(),
            })
            log(f"✅ 已注册 watch: {cal['label']} → 过期 {expires.isoformat()}")
        except urllib.error.HTTPError as e:
            err = e.read().decode()
            log(f"❌ 注册 watch 失败 ({cal['label']}): {e.code} {err}")

    # 保存状态
    state = {
        "ngrok_url": ngrok_url,
        "channels": results,
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    return results


class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """GET / → 健康检查"""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Meeting Assistant Calendar Webhook")
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        """POST /calendar-webhook → Google Calendar 推送通知"""
        if self.path == "/calendar-webhook":
            resource_state = self.headers.get("X-Goog-Resource-State", "")
            channel_id = self.headers.get("X-Goog-Channel-ID", "")
            resource_id = self.headers.get("X-Goog-Resource-ID", "")

            log(f"📩 收到推送: state={resource_state} channel={channel_id[:8]}...")

            if resource_state == "sync":
                # 初始同步通知（频道创建时）
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
                return

            # 非初始同步 → 触发日历同步
            if resource_state in ("update", "exists"):
                threading.Thread(target=do_sync, daemon=True).start()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, fmt, *args):
        """静的 access log 不打印"""
        pass


def run_server(port):
    server = HTTPServer(("0.0.0.0", port), WebhookHandler)
    log(f"🌐 Webhook 服务器启动: http://0.0.0.0:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Calendar webhook server")
    parser.add_argument("port", type=int, nargs="?", default=8899, help="本地端口")
    parser.add_argument("--ngrok-url", help="ngrok 公网 URL（首次启动时注册 watch 频道）")
    args = parser.parse_args()

    # 首次启动：注册 watch + 初始同步
    if args.ngrok_url:
        log("🔄 首次启动：注册 watch 频道...")
        register_watch(args.ngrok_url)
        log("🔄 执行初始同步...")
        do_sync()
    else:
        # 后续启动：加载已注册的频道信息
        if STATE_PATH.exists():
            state = json.loads(STATE_PATH.read_text())
            log(f"📋 已注册 {len(state.get('channels', []))} 个 watch 频道")
            # 检查是否过期（7 天）
            for ch in state.get("channels", []):
                expires = datetime.fromisoformat(ch["expires"])
                if expires < datetime.now(timezone.utc):
                    log(f"⚠️ 频道过期: {ch['label']} (于 {ch['expires']})")
                    log("   ngrok URL 未变的话重启 webhook 时加 --ngrok-url 重新注册")
        else:
            log("⚠️ 未注册 watch 频道，需要 --ngrok-url 参数首次启动")

    run_server(args.port)


if __name__ == "__main__":
    main()
