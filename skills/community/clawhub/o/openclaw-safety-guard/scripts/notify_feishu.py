#!/usr/bin/env python3
"""
Reads latest_status.json and sends a Feishu DM to 硕哥.
- Normal scan: report summary + dashboard path
- Score recovery: 恭喜 tone if score improved >= threshold
- Uses FEISHU_APP_ID + FEISHU_APP_SECRET from env (inherited from Gateway)
"""
import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime
from utils import get_data_dir, get_watchdog_config, get_workspace_root


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    if data.get("code") != 0:
        raise RuntimeError(f"Failed to get token: {data}")
    return data["tenant_access_token"]


def send_feishu_message(token: str, receive_id_type: str, receive_id: str, text: str) -> dict:
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}"
    payload = json.dumps({
        "receive_id": receive_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}),
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def load_env_fallback(var_names: list[str]) -> dict[str, str]:
    """Load selected vars from workspace .env when current process env is missing them."""
    env_path = Path(get_workspace_root()) / ".env"
    if not env_path.exists():
        return {}

    loaded = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key not in var_names or key in loaded:
            continue
        loaded[key] = value.strip().strip("'").strip('"')
    return loaded


def build_message(data: dict, dashboard_path: str) -> str:
    score = data.get("global_score", 0)
    previous_score = data.get("previous_score")
    score_delta = data.get("score_delta", 0)
    stats = data.get("stats", {})
    open_issues = stats.get("current_open", 0)
    total_resolved = stats.get("total_resolved", 0)
    active_issues = data.get("active_issues", [])
    generated_at = data.get("generated_at", "")[:16].replace("T", " ")

    score_icon = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"

    # Recovery tone vs normal tone
    config = get_watchdog_config()
    threshold = config.get("notify", {}).get("score_recovery_threshold", 3)

    if previous_score is not None and score_delta >= threshold:
        header = (
            f"🎉 恭喜硕哥！龙虾健康分从 {previous_score} 分升到了 {score} 分（↑+{score_delta}）"
            f"\n扫描时间：{generated_at}"
        )
    else:
        delta_str = ""
        if previous_score is not None and score_delta != 0:
            delta_str = f"（{'↑+' if score_delta > 0 else '↓'}{score_delta}）"
        header = (
            f"{score_icon} OpenClaw 安全卫士每日体检报告"
            f"\n扫描时间：{generated_at}"
            f"\n系统健康分：{score}/100{delta_str}"
        )

    stats_line = f"待处理：{open_issues} 个 | 历史已修复：{total_resolved} 个"

    issues_lines = ""
    if active_issues:
        issues_lines = "\n\n🔥 当前问题：\n"
        for iss in active_issues[:5]:
            sev = iss.get("severity", "LOW")
            sev_icon = "🔴" if sev == "HIGH" else "🟡" if sev == "MEDIUM" else "🔵"
            dim = iss.get("dimension", "")
            days = iss.get("days_open", 0)
            days_str = f"，已 {days} 天" if days > 0 else ""
            issues_lines += f"{sev_icon} [{sev}] {iss.get('title', '')}（{dim}{days_str}）\n"
        if open_issues > 5:
            issues_lines += f"... 还有 {open_issues - 5} 个问题"
    else:
        issues_lines = "\n\n✅ 系统完全健康，无任何问题！"

    dashboard_line = f"\n\n📊 Dashboard（仅限电脑端打开）：\nfile://{dashboard_path}"
    cursor_hint = "\n\n💡 把问题日志拖到 Cursor 修复后，在本群回复「体检」重新扫描。"

    return header + "\n" + stats_line + issues_lines + dashboard_line + cursor_hint


def main():
    config = get_watchdog_config()
    notify_cfg = config.get("notify", {})

    if not notify_cfg.get("enabled", True):
        print("Feishu notify is disabled in config.json")
        return

    app_id_env = notify_cfg.get("app_id_env", "FEISHU_APP_ID")
    app_secret_env = notify_cfg.get("app_secret_env", "FEISHU_APP_SECRET")
    app_id = os.environ.get(app_id_env, "")
    app_secret = os.environ.get(app_secret_env, "")
    if not app_id or not app_secret:
        fallback = load_env_fallback([app_id_env, app_secret_env])
        app_id = app_id or fallback.get(app_id_env, "")
        app_secret = app_secret or fallback.get(app_secret_env, "")

    if not app_id or not app_secret:
        print(f"WARN: {app_id_env} or {app_secret_env} not set, skipping Feishu notify")
        return

    receive_id_type = notify_cfg.get("receive_id_type", "open_id")
    receive_id = notify_cfg.get("receive_id", "")
    if not receive_id:
        print("WARN: notify.receive_id not configured in config.json, skipping")
        return

    data_dir = get_data_dir()
    status_path = os.path.join(data_dir, "latest_status.json")
    dashboard_path = os.path.join(data_dir, "dashboard.html")

    if not os.path.exists(status_path):
        print(f"WARN: {status_path} not found, skipping notify")
        return

    with open(status_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    message = build_message(data, dashboard_path)

    print("Getting Feishu token...")
    try:
        token = get_tenant_access_token(app_id, app_secret)
    except Exception as e:
        print(f"ERROR: Failed to get Feishu token: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Sending Feishu message to {receive_id_type}={receive_id}...")
    try:
        result = send_feishu_message(token, receive_id_type, receive_id, message)
        if result.get("code") == 0:
            print("✅ Feishu notify sent successfully")
        else:
            print(f"ERROR: Feishu API returned error: {result}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to send Feishu message: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
