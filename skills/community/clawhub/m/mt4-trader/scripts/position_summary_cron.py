#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持仓汇总 - 消息推送版本

通过 Webhook 将持仓汇总推送到消息通道（微信等）。
使用环境变量配置凭证，避免硬编码。

环境变量:
  SUMMARY_WEBHOOK_URL   - Webhook 接口地址 (默认 http://localhost:1608/api/message/send)
  SUMMARY_USER_ID       - 接收消息的用户 ID
  SUMMARY_ACCOUNT_ID    - 发送账号 ID
  SUMMARY_CHANNEL       - 消息通道 (默认 openclaw-weixin)

依赖: mt4_client.py, summary_utils.py
"""
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mt4_client import MT4Client
from summary_utils import build_position_summary

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("position_summary_cron")

# ---- 配置 ----
WEBHOOK_URL = os.environ.get(
    "SUMMARY_WEBHOOK_URL",
    "http://localhost:1608/api/message/send"
)
USER_ID = os.environ.get("SUMMARY_USER_ID", "")
ACCOUNT_ID = os.environ.get("SUMMARY_ACCOUNT_ID", "")
CHANNEL = os.environ.get("SUMMARY_CHANNEL", "openclaw-weixin")


def send_message(msg):
    """通过 Webhook 发送消息。"""
    if not USER_ID or not ACCOUNT_ID:
        logger.warning("SUMMARY_USER_ID 或 SUMMARY_ACCOUNT_ID 未设置，跳过消息发送。")
        logger.info("消息内容:\n%s", msg)
        return True

    try:
        import requests
    except ImportError:
        logger.error("缺少 requests 库，无法发送消息。请执行: pip install requests")
        return False

    payload = {
        "action": "send",
        "channel": CHANNEL,
        "to": USER_ID,
        "message": msg,
        "accountId": ACCOUNT_ID
    }
    try:
        resp = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        if resp.status_code == 200:
            logger.info("消息发送成功")
            return True
        else:
            logger.error("消息发送失败，HTTP %s: %s", resp.status_code, resp.text[:200])
            return False
    except requests.exceptions.Timeout:
        logger.error("消息发送超时（%s）", WEBHOOK_URL)
        return False
    except requests.exceptions.ConnectionError:
        logger.error("无法连接到 Webhook 服务: %s", WEBHOOK_URL)
        return False
    except Exception as e:
        logger.exception("消息发送异常")
        return False


def main():
    logger.info("开始获取持仓数据...")
    c = MT4Client()

    try:
        r = c.get_positions()
    except Exception as e:
        logger.exception("获取持仓失败")
        send_message(f"❌ 获取持仓失败: {e}")
        return

    summary, count, total_pl = build_position_summary(r)

    if count == 0:
        msg = "✅ 当前已空仓，停止发送订单汇总。"
        logger.info(msg)
    else:
        msg = summary

    send_message(msg)


if __name__ == "__main__":
    main()