#!/usr/bin/env python3
"""
Aligenie 消息推送服务器
接收 OpenClaw 的推送请求，调用阿里云 API 让天猫精灵播报

依赖: flask, requests
安装: pip install flask requests
运行: python push-server.py --port 5000
"""

import argparse
import logging
import json
import time
from typing import Optional

try:
    import requests
except ImportError:
    print("❌ 需要安装依赖: pip install flask requests")
    raise

try:
    from flask import Flask, request, jsonify
except ImportError:
    print("❌ 需要安装 flask: pip install flask")
    raise

_LOGGER = logging.getLogger(__name__)

app = Flask(__name__)

# ── 配置 ──────────────────────────────────────────────────

# 阿里云 OAuth2 获取 access_token 的地址
TOKEN_URL = "https://oauth.taobao.com/token"
# Aligenie 消息推送 API 地址
PUSH_API_URL = "https://api.aligenie.com/v1.0/push/pushMsg"

# 内存缓存 token（避免每次请求都重新认证）
_access_token_cache = {
    "token": None,
    "expires_at": 0,
}


# ── 阿里云 API 封装 ───────────────────────────────────────

def get_access_token(app_id: str, app_secret: str) -> Optional[str]:
    """获取阿里云 access_token（带缓存）"""
    now = time.time()

    if _access_token_cache["token"] and _access_token_cache["expires_at"] > now + 60:
        return _access_token_cache["token"]

    try:
        resp = requests.get(
            TOKEN_URL,
            params={
                "grant_type": "client_credentials",
                "client_id": app_id,
                "client_secret": app_secret,
            },
            timeout=10,
        )
        data = resp.json()
        if "access_token" in data:
            _access_token_cache["token"] = data["access_token"]
            _access_token_cache["expires_at"] = now + data.get("expires_in", 3600)
            _LOGGER.info("成功获取 access_token")
            return data["access_token"]
        else:
            _LOGGER.error(f"获取 access_token 失败: {data}")
            return None
    except Exception as e:
        _LOGGER.error(f"获取 access_token 异常: {e}")
        return None


def push_message(
    access_token: str,
    open_id: str,
    text: str,
    device_type: str = "speaker",
) -> dict:
    """
    调用 Aligenie 消息推送 API

    device_type: "speaker"=无屏音箱, "screen"=带屏设备
    """
    try:
        resp = requests.post(
            PUSH_API_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={
                "openId": open_id,
                "msgType": "text",
                "content": text,
                "deviceType": device_type,
            },
            timeout=15,
        )
        result = resp.json()
        _LOGGER.info(f"Aligenie API 响应: {result}")
        return result

    except Exception as e:
        _LOGGER.error(f"调用 Aligenie API 异常: {e}")
        return {"success": False, "error": str(e)}


# ── Flask 路由 ────────────────────────────────────────────

@app.route("/health")
def health():
    """健康检查"""
    return jsonify({"status": "ok", "service": "aligenie-push-server"})


@app.route("/push", methods=["POST"])
def handle_push():
    """
    接收 OpenClaw 的推送请求

    请求体:
    {
        "appId": "2026032918608",
        "appSecret": "xxx",
        "openId": "ou_xxx",
        "text": "要播报的内容",
        "deviceType": "speaker"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "请求体为空"}), 400

        app_id = data.get("appId") or os.environ.get("ALIGENIE_APP_ID", "")
        app_secret = data.get("appSecret") or os.environ.get("ALIGENIE_APP_SECRET", "")
        open_id = data.get("openId") or os.environ.get("ALIGENIE_DEVICE_OPEN_ID", "")
        text = data.get("text", "").strip()
        device_type = data.get("deviceType", "speaker")

        if not text:
            return jsonify({"success": False, "error": "text 不能为空"}), 400
        if not open_id:
            return jsonify({"success": False, "error": "openId 不能为空"}), 400

        # 优先用请求体里的凭证，否则用环境变量
        _app_id = app_id or os.environ.get("ALIGENIE_APP_ID", "")
        _app_secret = app_secret or os.environ.get("ALIGENIE_APP_SECRET", "")

        if not _app_id or not _app_secret:
            return jsonify({
                "success": False,
                "error": "AppId 或 AppSecret 未配置"
            }), 400

        # 获取 token 并推送
        access_token = get_access_token(_app_id, _app_secret)
        if not access_token:
            return jsonify({"success": False, "error": "获取 access_token 失败"}), 500

        result = push_message(access_token, open_id, text, device_type)

        if result.get("success") or result.get("returnCode") == 0:
            return jsonify({
                "success": True,
                "messageId": result.get("messageId", ""),
            })
        else:
            return jsonify({
                "success": False,
                "error": result.get("errorMessage") or result.get("returnValue", str(result)),
            }), 500

    except Exception as e:
        _LOGGER.exception("处理推送请求异常")
        return jsonify({"success": False, "error": str(e)}), 500


# ── 主入口 ────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Aligenie 消息推送服务器")
    parser.add_argument("--port", type=int, default=5000, help="监听端口 (默认: 5000)")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址 (默认: 0.0.0.0)")
    parser.add_argument("--debug", action="store_true", help="开启调试模式")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    _LOGGER.info(f"启动 Aligenie 推送服务器，监听 {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    import os
    main()
