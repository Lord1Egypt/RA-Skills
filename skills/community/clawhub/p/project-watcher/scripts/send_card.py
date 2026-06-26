#!/usr/bin/env python3
"""
发送飞书交互卡片。
用法: python3 send_card.py <receive_id> <title> <project> <branch> <short_hash> <message> [repo_url]

凭证从环境变量读取，fallback 到 configs/feishu.json（由 SKILL.md 管理）。
"""
import sys, json, urllib.request, os

API_BASE = "https://open.feishu.cn/open-apis"
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../configs/feishu.json")

def load_credentials():
    """从环境变量或配置文件读取飞书凭证。"""
    app_id = os.environ.get("FEISHU_APP_ID") or os.environ.get("APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET") or os.environ.get("APP_SECRET")
    if app_id and app_secret:
        return app_id, app_secret
    # Fallback 到配置文件
    try:
        with open(CONFIG_PATH) as f:
            cfg = json.load(f)
            return cfg.get("app_id", ""), cfg.get("app_secret", "")
    except Exception:
        return "", ""

def get_token():
    app_id, app_secret = load_credentials()
    if not app_id or not app_secret:
        raise RuntimeError("Feishu credentials not found (env vars or configs/feishu.json)")
    req = urllib.request.Request(
        f"{API_BASE}/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": app_id, "app_secret": app_secret}).encode(),
        headers={"Content-Type": "application/json"}
    )
    resp = json.loads(urllib.request.urlopen(req).read())
    token = resp.get("tenant_access_token", "")
    if not token:
        raise RuntimeError("Failed to obtain tenant access token")
    return token

def send_card(receive_id, title, project, branch, short_hash, message, repo_url=None):
    token = get_token()

    repo_line = f"\n**仓库：** {repo_url}" if repo_url else ""
    # title 不重复放在 body 里，只留标签行
    card_body_elements = [
        {"tag": "markdown", "content": f"**{title}**\n\n**项目：** {project}\n**分支：** {branch}\n**提交：** `{short_hash}`\n**消息：** {message}{repo_line}"}
    ]

    card = {
        "schema": "2.0",
        "config": {"wide_screen_mode": True},
        "body": {"elements": card_body_elements}
    }

    payload = {
        "receive_id": receive_id,
        "msg_type": "interactive",
        "content": json.dumps(card)
    }

    # receive_id_type 只能是 open_id（scope 限制），user_id 会 scope 错误
    for id_type in ["open_id", "user_id"]:
        req = urllib.request.Request(
            f"{API_BASE}/im/v1/messages?receive_id_type={id_type}",
            data=json.dumps(payload).encode(),
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )
        try:
            resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
            code = resp.get("code")
            if code == 0:
                return code, resp.get("msg"), resp.get("data", {}).get("message_id")
            # 9986004 = scope 无权限，尝试换 ID 类型
            if code == 9986004 or "scope" in resp.get("msg", "").lower():
                continue
            # 其他错误直接返回，不继续试
            return code, resp.get("msg"), resp.get("data", {}).get("message_id")
        except Exception as e:
            return -1, str(e), ""
    return -1, "All ID types failed", ""

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: send_card.py <receive_id> <title> <project> <branch> <short_hash> <message> [repo_url]")
        sys.exit(1)

    receive_id = sys.argv[1]
    title = sys.argv[2]
    project = sys.argv[3]
    branch = sys.argv[4]
    short_hash = sys.argv[5]
    message = sys.argv[6]
    repo_url = sys.argv[7] if len(sys.argv) > 7 else None

    code, msg, mid = send_card(receive_id, title, project, branch, short_hash, message, repo_url)
    print(f"Code: {code}, Msg: {msg}, Message ID: {mid}")
