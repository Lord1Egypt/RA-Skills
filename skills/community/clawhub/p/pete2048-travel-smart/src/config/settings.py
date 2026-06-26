# -*- coding: utf-8 -*-
"""
配置管理
"""
import os
import yaml
from pathlib import Path
from loguru import logger

PROJECT_ROOT = Path(__file__).parent.parent.parent


def load_api_keys():
    """加载 API Keys"""
    config_path = PROJECT_ROOT / "config" / "api_keys.yaml"
    if not config_path.exists():
        logger.warning(f"配置文件不存在: {config_path}，使用环境变量")
        return {}
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# ---- 高德配置 ----
AMAP_KEY = os.getenv("AMAP_KEY", "") or load_api_keys().get("amap", {}).get("key", "")
AMAP_JS_KEY = os.getenv("AMAP_JS_KEY", "") or load_api_keys().get("amap", {}).get("js_key", "")
AMAP_BASE_URL = "https://restapi.amap.com/v3"

# ---- LLM 配置 ----
LLM_CONFIG = {
    "provider": os.getenv("LLM_PROVIDER", "minimax"),
    "api_key": os.getenv("MINIMAX_API_KEY", "") or load_api_keys().get("llm", {}).get("api_key", ""),
    "base_url": os.getenv("LLM_BASE_URL", "https://api.minimaxi.com"),
    "model": os.getenv("LLM_MODEL", "MiniMax-M2.7-highspeed"),
}

# ---- 评分权重配置 ----
# ---- 评分权重配置 ----
SCORING_WEIGHTS = {
    "highway": {"distance": 0.35, "rating": 0.35, "price": 0.0, "detour": 0.30},
    "hotel": {"distance": 0.20, "rating": 0.20, "price": 0.30, "next_day": 0.30},
    "taxi": {"distance": 0.40, "rating": 0.20, "price": 0.10, "detour": 0.30},
}
