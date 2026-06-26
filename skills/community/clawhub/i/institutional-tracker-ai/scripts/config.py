"""机构操盘行为识别算法 - 配置文件"""
import os
from pathlib import Path

# === 路径配置 ===
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SCORES_DIR = DATA_DIR / "daily_scores"
STATE_DIR = DATA_DIR / "state_history"
REPORTS_DIR = BASE_DIR / "reports"

# === 数据源配置 ===
TUSHARE_TOKEN = "YOUR_TUSHARE_TOKEN_HERE"  # 替换为你的 Tushare 代理 Token
TUSHARE_API_URL = "YOUR_TUSHARE_API_URL"   # 替换为你的代理 API 地址
TUSHARE_RATE_LIMIT = 0.6  # 每次请求间隔（秒），120次/分钟=0.5s，留余量

# NeoData 查询脚本路径
NEODATA_SCRIPT = Path(os.path.expanduser(
    "~/.workbuddy/plugins/marketplaces/cb_teams_marketplace/plugins/finance-data/skills/neodata-financial-search/scripts/query.py"
))

# === 算法参数 ===
# 信号评分权重 (v5调整)
WEIGHTS = {
    "fund_flow": 0.30,      # 资金结构分析（核心）
    "volume_price": 0.24,   # 量价形态识别
    "chip_dist": 0.18,      # 筹码/位置分析（降低：需更多历史数据才精准）
    "north_margin": 0.16,   # 北向+融资融券（提高：融资数据已接入）
    "event": 0.12,          # 事件/异动（提高：已接入更多信号）
}

# 状态转换阈值
THRESHOLDS = {
    "accumulation_enter": 30,    # 进入吸筹状态
    "washout_range": (10, 50),   # 洗盘区间
    "markup_enter": 50,          # 进入拉升状态
    "distribution_enter": -20,   # 进入出货状态
    "neutral_range": (-10, 10),  # 观望区
}

# 连续确认天数（防止单日噪音）
CONFIRM_DAYS = 2

# 监控池大小
POOL_SIZE = {
    "top_sectors": 8,        # 取 TOP N 板块
    "stocks_per_sector": 5,  # 每个板块取 N 只龙头
    "north_top": 10,         # 北向 TOP N
}

# === 用户自定义关注股 ===
WATCHLIST = [
    # 可以在这里添加你特别关注的股票代码
    # "300750.SZ",  # 宁德时代
    # "002594.SZ",  # 比亚迪
]
