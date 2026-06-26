import json
import os
import sys
import urllib.request
from pathlib import Path


def get_token(app_id, app_secret):
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": app_id, "app_secret": app_secret}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    token = data.get("tenant_access_token")
    if not token:
        raise RuntimeError(f"Token error: {data}")
    return token


def send_text(token, receiver, text):
    payload = {
        "receive_id": receiver,
        "msg_type": "text",
        "content": json.dumps({"text": text}, ensure_ascii=False),
    }
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Send failed (HTTP {e.code}): {err_body}")
    if data.get("code") != 0:
        raise RuntimeError(f"Send failed: {data}")
    return data


def main():
    if len(sys.argv) < 2:
        print("Usage: python send_text.py <text or json>")
        sys.exit(1)

    raw = sys.argv[1]
    env_text = os.getenv("MURASAME_TEXT")
    if env_text:
        text = env_text
    else:
        try:
            obj = json.loads(raw)
            text = obj.get("text", "") if isinstance(obj, dict) else raw
        except Exception:
            text = raw
    if text == "_":
        text = ""
    text = text.strip()
    # debug
    try:
        Path(r"C:\Users\chenxun\.nanobot\workspace\murasame_text_debug.txt").write_text(repr(text), encoding="utf-8")
    except Exception:
        pass
    if not text:
        print("SKIP_EMPTY")
        return
    receiver = os.getenv("FEISHU_RECEIVER")
    if not receiver:
        raise SystemExit("Missing FEISHU_RECEIVER")

    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    if not app_id or not app_secret:
        raise SystemExit("Missing FEISHU_APP_ID or FEISHU_APP_SECRET")

    token = get_token(app_id, app_secret)
    send_text(token, receiver, text)
    print("OK: sent text")


if __name__ == "__main__":
    main()
