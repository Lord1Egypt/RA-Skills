# -*- coding: utf-8 -*-
"""
Stock Monitor Pro - 配置示例文件

使用说明:
1. 复制此文件为 config.py
2. 修改 WATCHLIST 中的持仓信息
3. 运行 ./control.sh start 启动监控
"""

# ============ 监控列表配置 ============

WATCHLIST = [
    # ===== 个股示例 =====
    {
        "code": "600362",
        "name": "江西铜业",
        "market": "sh",
        "type": "individual",  # 个股
        "cost": 57.00,         # 你的持仓成本
        "alerts": {
            "cost_pct_above": 15.0,    # 盈利 15% 提醒
            "cost_pct_below": -12.0,   # 亏损 12% 提醒
            "change_pct_above": 4.0,   # 日内上涨 4% 提醒
            "change_pct_below": -4.0,  # 日内下跌 4% 提醒
            "volume_surge": 2.0,       # 放量 2 倍提醒
            # 以下为付费功能
            "ma_monitor": True,        # 均线金叉死叉
            "rsi_monitor": True,       # RSI 超买超卖
            "gap_monitor": True,       # 跳空缺口
            "trailing_stop": True      # 动态止盈
        }
    },
    
    # ===== ETF 示例 =====
    {
        "code": "159892",
        "name": "恒生医疗",
        "market": "sz",
        "type": "etf",       # ETF
        "cost": 0.80,
        "alerts": {
            "cost_pct_above": 15.0,
            "cost_pct_below": -15.0,
            "change_pct_above": 2.0,   # ETF 波动小，阈值更低
            "change_pct_below": -2.0,
            "volume_surge": 1.8
        }
    },
    
    # ===== 伦敦金示例 =====
    {
        "code": "XAU",
        "name": "伦敦金 (人民币/克)",
        "market": "fx",
        "type": "gold",       # 黄金
        "cost": 4650.0,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -8.0,
            "change_pct_above": 2.5,
            "change_pct_below": -2.5
            # 黄金不监控成交量
        }
    },
]

# ============ 智能频率配置 (一般无需修改) ============

SMART_SCHEDULE = {
    "market_open": {
        "hours": [(9, 30), (11, 30), (13, 0), (15, 0)],
        "interval": 300  # 交易时间：5 分钟
    },
    "after_hours": {
        "interval": 1800  # 收盘后：30 分钟
    },
    "night": {
        "hours": [(0, 0), (8, 0)],
        "interval": 3600  # 凌晨：1 小时 (仅伦敦金)
    },
}

# ============ 消息推送配置 (可选) ============

# Feishu 推送 (如需推送到飞书)
FEISHU_WEBHOOK = None  # 填入你的飞书 webhook URL

# 邮件推送 (如需邮件通知)
EMAIL_CONFIG = {
    "enabled": False,
    "smtp_server": "smtp.example.com",
    "smtp_port": 587,
    "username": "your_email@example.com",
    "password": "your_password",
    "recipients": ["recipient@example.com"]
}

# ============ 其他配置 ============

# 日志级别：DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = "INFO"

# 日志文件路径
LOG_FILE = "monitor.log"

# 预警防骚扰：同类预警间隔 (秒)
ALERT_COOLDOWN = 1800  # 30 分钟
