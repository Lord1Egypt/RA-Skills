"""
配置管理器 - 管理 Riot API Key 和用户配置
"""
import os
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".lol-analyst"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "riot_api_key": "",
    "default_region": "kr",
    "default_language": "zh_CN",
    "cache_enabled": True,
}

# 区域映射
REGIONS = {
    "br1": "巴西", "eun1": "北欧/东欧", "euw1": "西欧",
    "jp1": "日本", "kr": "韩国", "la1": "拉丁美洲北",
    "la2": "拉丁美洲南", "na1": "北美", "oc1": "大洋洲",
    "tr1": "土耳其", "ru": "俄罗斯", "ph2": "菲律宾",
    "sg2": "新加坡", "th2": "泰国", "tw2": "中国台湾",
    "vn2": "越南",
}

# 区域对应的路由值 (用于 Riot API)
REGION_ROUTING = {
    "br1": "americas", "la1": "americas", "la2": "americas", "na1": "americas",
    "eun1": "europe", "euw1": "europe", "tr1": "europe", "ru": "europe",
    "jp1": "asia", "kr": "asia",
    "oc1": "sea", "ph2": "sea", "sg2": "sea", "th2": "sea", "tw2": "sea", "vn2": "sea",
}

# 排位缩写
TIER_NAMES = {
    "IRON": "黑铁", "BRONZE": "青铜", "SILVER": "白银",
    "GOLD": "黄金", "PLATINUM": "铂金", "EMERALD": "翡翠",
    "DIAMOND": "钻石", "MASTER": "大师", "GRANDMASTER": "宗师",
    "CHALLENGER": "王者",
}

RANK_NAMES = {"I": "一", "II": "二", "III": "三", "IV": "四"}

QUEUE_NAMES = {
    "RANKED_SOLO_5x5": "单双排",
    "RANKED_FLEX_SR": "灵活排位",
    "RANKED_TFT": "云顶之弈",
    "RANKED_TFT_TURBO": "云顶之弈(狂暴)",
}


def load_config():
    """加载配置文件，不存在则创建默认配置"""
    if not CONFIG_FILE.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        # 合并默认值
        merged = DEFAULT_CONFIG.copy()
        merged.update(config)
        return merged
    except (json.JSONDecodeError, IOError):
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """保存配置到文件"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_api_key():
    """获取 API Key：优先级 环境变量 > 配置文件"""
    env_key = os.environ.get("RIOT_API_KEY", "")
    if env_key:
        return env_key

    config = load_config()
    return config.get("riot_api_key", "")


def set_api_key(api_key: str):
    """保存 API Key 到配置文件"""
    config = load_config()
    config["riot_api_key"] = api_key
    save_config(config)


def get_routing(region: str) -> str:
    """获取区域对应的路由值"""
    return REGION_ROUTING.get(region.lower(), region.lower())


def get_region_name(region: str) -> str:
    """获取区域中文名称"""
    return REGIONS.get(region.lower(), region.upper())


def tier_cn(tier: str) -> str:
    """排位中文名"""
    return TIER_NAMES.get(tier.upper(), tier)


def rank_cn(rank: str) -> str:
    """段位中文名"""
    return RANK_NAMES.get(rank.upper(), rank)


def queue_cn(queue: str) -> str:
    """队列类型中文名"""
    return QUEUE_NAMES.get(queue, queue)
