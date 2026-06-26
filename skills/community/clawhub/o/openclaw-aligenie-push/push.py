#!/usr/bin/env python3
"""
openclaw-aligenie-push: 向天猫精灵设备推送语音播报

依赖: requests
安装: pip install requests
"""

import os
import json
import logging
import asyncio
from typing import Optional

try:
    import requests
except ImportError:
    print("❌ 需要安装 requests: pip install requests")
    raise

_LOGGER = logging.getLogger(__name__)

# ── 配置读取 ──────────────────────────────────────────────

def _read_config():
    """从环境变量或 TOOLS.md 配置文件读取配置"""
    # 优先读环境变量（部署时用）
    push_server = os.environ.get("ALIGENIE_PUSH_SERVER", "")
    app_id = os.environ.get("ALIGENIE_APP_ID", "")
    app_secret = os.environ.get("ALIGENIE_APP_SECRET", "")
    device_open_id = os.environ.get("ALIGENIE_DEVICE_OPEN_ID", "")

    # 尝试从 TOOLS.md 读取（本地开发用）
    tools_md = os.path.expanduser("~/.openclaw/workspace/TOOLS.md")
    if os.path.exists(tools_md):
        with open(tools_md) as f:
            content = f.read()

        import re
        patterns = {
            "push_server": r"ALIGENIE_PUSH_SERVER\s*=\s*(.+?)(?:\n|$)",
            "app_id": r"ALIGENIE_APP_ID\s*=\s*(.+?)(?:\n|$)",
            "app_secret": r"ALIGENIE_APP_SECRET\s*=\s*(.+?)(?:\n|$)",
            "device_open_id": r"ALIGENIE_DEVICE_OPEN_ID\s*=\s*(.+?)(?:\n|$)",
        }
        for key, pat in patterns.items():
            val = re.search(pat, content)
            if val and not locals()[key]:
                locals()[key] = val.group(1).strip()

    return {
        "push_server": push_server,
        "app_id": app_id,
        "app_secret": app_secret,
        "device_open_id": device_open_id,
    }


# ── 主要推送函数 ──────────────────────────────────────────

async def push(
    text: str,
    device_type: str = "speaker",
    open_id: Optional[str] = None,
    app_id: Optional[str] = None,
    app_secret: Optional[str] = None,
    push_server: Optional[str] = None,
) -> dict:
    """
    向天猫精灵设备推送语音播报。

    参数:
        text: 要播报的文字内容
        device_type: "speaker"=无屏音箱, "screen"=带屏设备
        open_id: 设备 openId（留空则用配置中的默认设备）
        app_id: Aligenie AppId（留空则用配置）
        app_secret: Aligenie AppSecret（留空则用配置）
        push_server: 云服务器推送地址（留空则用配置）

    返回:
        {"success": True, "messageId": "xxx"}
        或 {"success": False, "error": "错误描述"}
    """
    config = _read_config()

    _push_server = push_server or config["push_server"]
    _app_id = app_id or config["app_id"]
    _app_secret = app_secret or config["app_secret"]
    _open_id = open_id or config["device_open_id"]

    # 验证必填项
    if not _push_server:
        return {
            "success": False,
            "error": "未配置 ALIGENIE_PUSH_SERVER，请先配置云服务器推送地址"
        }
    if not _open_id:
        return {
            "success": False,
            "error": "未配置设备 openId，请在 TOOLS.md 或环境变量中设置 ALIGENIE_DEVICE_OPEN_ID"
        }

    payload = {
        "appId": _app_id or "",
        "appSecret": _app_secret or "",
        "openId": _open_id,
        "text": text,
        "deviceType": device_type,
    }

    _LOGGER.info(f"[Aligenie Push] 发送播报请求: {text[:50]}...")

    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(
                _push_server,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15,
            )
        )

        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                _LOGGER.info(f"[Aligenie Push] 成功: {result.get('messageId', 'N/A')}")
                return {"success": True, "messageId": result.get("messageId")}
            else:
                _LOGGER.error(f"[Aligenie Push] 推送失败: {result.get('error')}")
                return {"success": False, "error": result.get("error", "未知错误")}
        else:
            _LOGGER.error(f"[Aligenie Push] HTTP错误: {response.status_code} - {response.text[:200]}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text[:200]}"
            }

    except requests.exceptions.Timeout:
        _LOGGER.error("[Aligenie Push] 请求超时")
        return {"success": False, "error": "请求超时，云服务器响应过慢"}
    except Exception as e:
        _LOGGER.error(f"[Aligenie Push] 异常: {e}")
        return {"success": False, "error": str(e)}


# ── CLI 测试入口 ──────────────────────────────────────────

if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if len(sys.argv) < 2:
        print("用法: python push.py <播报内容>")
        print("示例: python push.py '任务已完成，请查看结果'")
        sys.exit(1)

    text = " ".join(sys.argv[1:])
    result = asyncio.run(push(text))
    print(json.dumps(result, ensure_ascii=False, indent=2))
