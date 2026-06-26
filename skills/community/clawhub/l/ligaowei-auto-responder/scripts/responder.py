#!/usr/bin/env python3
"""
ligaowei-auto-responder — 李高伟飞书自动回复助手（私聊版）

Usage:
  responder.py --once            # 处理一次（配合 cron）
  responder.py --dry-run         # 模拟运行，不发送
  responder.py --hook <json>     # 钩子模式，接收消息 JSON
  responder.py --clear-cache     # 清除缓存
"""
import json
import os
import sys
import time
import re
from pathlib import Path

CACHE_DIR = Path.home() / ".cache"
CACHE_FILE = CACHE_DIR / "ligaowei-auto-responder.json"
CONFIG_FILE = Path.cwd() / "ligaowei-auto-responder.json"

# 默认配置模板
DEFAULT_CONFIG = {
    "enabled": True,
    "dm_only": True,
    "globalCooldownMinutes": 1,
    "maxResponsesPerMinute": 10,
    "topics": {
        "商户问题": {
            "keywords": ["商户", "商家", "费率", "结算", "退款", "交易", "流水", "收款"],
            "responseTemplate": "此为ai助手自动回复，若有疑义，稍后联系"
        },
        "到账打款": {
            "keywords": ["到账", "打款"],
            "responseTemplate": "本消息由 AI 自动生成，仅供参考\n每月20号左右打款，若有问题可咨询涂雅青"
        }
    }
}


def load_config():
    """加载配置，如果不存在则用默认模板"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return DEFAULT_CONFIG


def load_cache():
    """加载缓存"""
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {"replies": {}}


def save_cache(cache):
    """保存缓存"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def match_keywords(text, keywords):
    """检查文本是否包含任一关键词"""
    text_lower = text.lower()
    for kw in keywords:
        if kw.lower() in text_lower:
            return True
    return False


def check_cooldown(cache, user_id, topic_name, cooldown_minutes):
    """检查冷却时间"""
    replies = cache.get("replies", {})
    key = f"{user_id}:{topic_name}"
    last_time = replies.get(key, 0)
    elapsed = time.time() - last_time
    return elapsed > cooldown_minutes * 60


def check_rate_limit(cache, max_per_minute):
    """检查每分钟速率限制"""
    replies = cache.get("replies", {})
    now = time.time()
    recent = sum(1 for t in replies.values() if now - t < 60)
    return recent < max_per_minute


def should_auto_respond(user_message, config):
    """检查是否应触发自动回复，返回匹配的 topic 和模板"""
    if not config.get("enabled", True):
        return None, None

    for topic_name, topic_config in config.get("topics", {}).items():
        keywords = topic_config.get("keywords", [])
        if match_keywords(user_message, keywords):
            return topic_name, topic_config.get("responseTemplate", "")

    return None, None


def handle_message(message_text, sender_id, sender_name=""):
    """
    处理单条消息的核心逻辑
    返回 (should_reply, reply_text, topic_name) 或 None
    """
    config = load_config()

    if not config.get("enabled", True):
        return None

    # 检查是否只处理私聊 (脚本调用方应已过滤)
    topic_name, template = should_auto_respond(message_text, config)
    if not topic_name:
        return None

    cache = load_cache()

    # 冷却检查
    cooldown = config.get("globalCooldownMinutes", 1)
    if not check_cooldown(cache, sender_id, topic_name, cooldown):
        return None

    # 速率检查
    max_rpm = config.get("maxResponsesPerMinute", 10)
    if not check_rate_limit(cache, max_rpm):
        return None

    # 构建回复
    reply = template
    reply = reply.replace("{topic}", topic_name)
    reply = reply.replace("{text}", message_text[:100])
    reply = reply.replace("{sender}", sender_name or "用户")

    # 记录缓存
    cache.setdefault("replies", {})
    cache[f"replies"][f"{sender_id}:{topic_name}"] = time.time()
    # 清理 24h 前的缓存
    now = time.time()
    cache["replies"] = {
        k: v for k, v in cache["replies"].items()
        if now - v < 86400
    }
    save_cache(cache)

    return (True, reply, topic_name)


def clear_cache():
    """清除缓存"""
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()
        print("✅ 缓存已清除")
    else:
        print("ℹ️  缓存不存在，无需清除")


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "--clear-cache":
        clear_cache()
        return

    if cmd == "--dry-run":
        # 模拟模式：打印配置信息
        config = load_config()
        topics = list(config.get("topics", {}).keys())
        print(f"🔍 [DRY RUN] ligaowei-auto-responder")
        print(f"   dm_only: {config.get('dm_only', True)}")
        print(f"   冷却时间: {config.get('globalCooldownMinutes', 1)} 分钟")
        print(f"   速率限制: {config.get('maxResponsesPerMinute', 10)} 条/分钟")
        print(f"   已配主题: {', '.join(topics)}")
        for t in topics:
            kws = config["topics"][t].get("keywords", [])
            print(f"     · {t}: {', '.join(kws)}")
        return

    if cmd == "--once":
        # 单次执行模式（配合 cron）
        print("ℹ️  --once 模式需要配合消息队列使用")
        return

    if cmd == "--hook":
        # 钩子模式：接收消息 JSON（通过 stdin 或参数）
        msg_json = sys.argv[2] if len(sys.argv) > 2 else sys.stdin.read()
        try:
            msg = json.loads(msg_json)
            text = msg.get("text", "")
            sender_id = msg.get("sender_id", "unknown")
            sender_name = msg.get("sender_name", "")

            result = handle_message(text, sender_id, sender_name)
            if result:
                should_reply, reply_text, topic_name = result
                output = {
                    "action": "reply",
                    "topic": topic_name,
                    "reply": reply_text
                }
                print(json.dumps(output, ensure_ascii=False))
            else:
                print(json.dumps({"action": "pass"}))

        except json.JSONDecodeError as e:
            print(json.dumps({"action": "error", "message": str(e)}),
                  file=sys.stderr)
            sys.exit(1)
        return

    print(f"❌ 未知命令: {cmd}")
    sys.exit(1)


if __name__ == "__main__":
    main()
