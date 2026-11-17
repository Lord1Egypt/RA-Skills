#!/usr/bin/env python3
"""
config.py — 外内比监控配置
修改这里的配置来定制你的监控股票和告警阈值
"""

# ============== 监控股票列表 ==============
# 格式: (股票代码, 名称)
# 沪市A股以6开头，深市以0或3开头
WATCHED_STOCKS = [
    ("600036", "招商银行"),   # 银行龙头
    ("601318", "中国平安"),   # 保险龙头
    ("002891", "中宠股份"),   # 宠物消费
    ("000625", "长安汽车"),   # 汽车
    ("600780", "通宝能源"),   # 电力
    ("000426", "兴业银锡"),   # 有色金属
]

# ============== 告警阈值 ==============
ALERT_THRESHOLDS = {
    # 主力建仓信号：外内比超过此值认为主力在建仓
    "outer_ratio_strong": 1.25,

    # 主力出逃信号：外内比低于此值认为主力在出逃
    "outer_ratio_danger": 0.50,

    # 大涨异动：涨幅超过此值触发告警
    "surge_up_pct": 9.0,

    # 大跌异动：跌幅超过此值触发告警
    "surge_down_pct": -5.0,

    # 量能异常：成交量较上一扫描时段放大超过此倍数
    "volume_surge_ratio": 2.0,
}

# ============== Webhook配置 ==============
# 飞书Webhook（可选，不配置则仅输出到终端）
FEISHU_WEBHOOK = ""

# 钉钉Webhook（可选）
DINGTALK_WEBHOOK = ""

# ============== 数据存储路径 ==============
# 外内比历史数据库
HISTORY_FILE = "~/.openclaw/memory/stocks/outer_ratio_history.json"

# 盘中快照（用于量能对比）
SNAPSHOT_FILE = "~/.openclaw/memory/stocks/intraday_snapshots.json"
