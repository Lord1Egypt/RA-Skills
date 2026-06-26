# -*- coding: utf-8 -*-
"""
配置示例文件
复制此文件为 config.py 并填入你的配置
"""

# ==================== 钉钉配置 ====================
# 钉钉 Webhook 地址（从钉钉机器人设置中获取）
WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_ACCESS_TOKEN"

# 钉钉加签密钥（以 SEC 开头，从钉钉机器人安全设置中获取）
SECRET = "SECxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# =================================================

# ==================== 监控配置 ====================
# 检查间隔（秒），默认 60 秒检查一次
CHECK_INTERVAL = 60

# Gateway 端口，默认 18789
GATEWAY_PORT = 18789

# Gateway URL，一般不需要修改
GATEWAY_URL = f"http://127.0.0.1:{GATEWAY_PORT}/"
# =================================================

# ==================== 通知配置 ====================
# 启动时发送报平安通知
NOTIFY_ON_STARTUP = True

# Gateway 掉线时发送通知
NOTIFY_ON_DOWN = True

# Gateway 恢复后发送通知
NOTIFY_ON_RECOVERY = True

# Gateway 重启失败时发送通知
NOTIFY_ON_FAILED = True

# 每天发送报平安通知（仅在 8-10 点发送）
NOTIFY_DAILY = True
# =================================================

# ==================== 日志配置 ====================
# 日志文件路径
# Windows: %USERPROFILE%\.openclaw\gateway-watchdog.log
# Linux/macOS: ~/.openclaw/gateway-watchdog.log
import os
LOG_FILE = os.path.join(os.path.expanduser("~"), ".openclaw", "gateway-watchdog.log")
# =================================================
