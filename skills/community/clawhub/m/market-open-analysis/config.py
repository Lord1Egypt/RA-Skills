#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config.py - 每日开盘分析配置文件

⚠️ 使用前请配置 API Key！
"""

# ============== API 配置 ==============

# ⚠️ 东方财富妙想 API Key（必填！）
# 获取方式：联系东方财富妙想官方申请
MX_API_KEY = "YOUR_MX_API_KEY_HERE"  # ← 请修改这里
MX_API_URL = "https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search"

# ============== 推送配置 ==============

# 默认推送用户 ID（必填！）
# 飞书格式：ou_xxxxxxxxxxxx
# 其他渠道请参考对应平台的用户 ID 格式
DEFAULT_TARGET = "YOUR_USER_ID_HERE"  # ← 请修改这里

# 推送渠道（可选）
# 支持：feishu, telegram, discord, slack, whatsapp 等
# 留空则使用 OpenClaw 默认渠道
DEFAULT_CHANNEL = ""  # ← 留空使用默认，或填写具体渠道

# ============== 时间配置 ==============

# 数据收集时间（cron 格式）
COLLECT_TIME = "0 5 * * 1-5"  # 交易日 5:00

# 推送时间（cron 格式）
PUSH_TIME = "30 5 * * 1-5"   # 交易日 5:30

# ============== 路径配置 ==============

# 工作目录
WORKSPACE_DIR = "~/openclaw/workspace"

# 数据存储目录
DATA_DIR = "data"

# 日志目录
LOGS_DIR = "logs"

# 报告目录
REPORTS_DIR = "reports"

# ============== 查询配置 ==============

# 查询的商品
COMMODITIES = ["XAU", "WTIOIL-FUT"]  # 黄金、WTI 原油

# 计价货币
CURRENCY = "USD"

# 美油查询关键词
WTI_QUERIES = [
    "WTI 原油 OPEC 产量",
    "原油 库存 数据",
    "美油 地缘政治",
    "原油 供应 中断"
]

# 黄金查询关键词
GOLD_QUERIES = [
    "黄金 美联储 利率",
    "黄金 非农 数据",
    "XAUUSD 地缘政治",
    "黄金 通胀 预期"
]
