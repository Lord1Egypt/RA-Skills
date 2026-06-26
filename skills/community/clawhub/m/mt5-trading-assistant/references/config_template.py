"""
MT5 Trading Assistant 配置模板

将此文件保存为 config.py 并填写您的MT5账户信息。
脚本将从此文件导入配置。
"""

# =========================
# MT5 账户配置
# =========================

# Exness 模拟账户示例
MT5_CONFIG = {
    # 账户信息
    "login": 277528870,                     # 您的MT5账户号码
    "password": "your_password_here",       # 您的MT5账户密码
    "server": "Exness-MT5Trial5",          # MT5服务器名称
    
    # 交易品种配置
    "symbol": "XAUUSDm",                    # 交易品种 (Exness黄金为XAUUSDm)
    
    # 默认交易参数
    "default_volume": 0.01,                 # 默认手数
    "default_deviation": 20,                # 默认价格偏差点数
    "default_magic": 100000,                # 默认订单魔法号
    
    # 风险管理
    "max_risk_per_trade": 0.02,             # 单笔交易最大风险比例 (2%)
    "max_daily_loss": 0.10,                 # 单日最大亏损比例 (10%)
    
    # 监控设置
    "refresh_interval": 5,                  # 监控刷新间隔(秒)
}

# =========================
# 经纪商特定配置
# =========================

# Exness 特定配置
EXNESS_CONFIG = {
    "symbol_suffix": "m",                   # 品种后缀 (Exness使用'm'后缀)
    "server_prefix": "Exness-MT5Trial",     # 服务器前缀
}

# IC Markets 配置示例
ICMARKETS_CONFIG = {
    "symbol": "XAUUSD",                     # IC Markets使用标准符号
    "server": "ICMarkets-MT5",              # IC Markets服务器
}

# =========================
# 脚本使用示例
# =========================
"""
使用示例:

1. 导入配置:
   from config import MT5_CONFIG

2. 在脚本中使用:
   login = MT5_CONFIG["login"]
   password = MT5_CONFIG["password"]
   server = MT5_CONFIG["server"]
"""

# =========================
# 安全注意事项
# =========================
"""
重要安全提示:
1. 不要将此文件提交到版本控制系统
2. 在生产环境中使用环境变量存储密码
3. 定期更改密码
4. 仅授予必要的权限
"""