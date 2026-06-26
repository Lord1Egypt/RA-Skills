from __future__ import annotations

import os

DEFAULT_BASE_URL = os.getenv("IMA_BASE_URL", "https://api.imastudio.com")
DEFAULT_IM_BASE_URL = os.getenv("IMA_IM_BASE_URL", "https://imapi.liveme.com")
PREFS_PATH = os.path.expanduser("~/.openclaw/memory/ima_prefs.json")

IMAGE_TASK_TYPES = ("text_to_image", "image_to_image")
DEFAULT_MODEL_BY_TASK_TYPE = {
    "text_to_image": "gpt-image-2",
    "image_to_image": "gpt-image-2",
}
DEFAULT_MODEL_LABEL_BY_TASK_TYPE = {
    "text_to_image": "GPT Image 2",
    "image_to_image": "GPT Image 2",
}
MODEL_PROFILE_BY_ID = {
    "gpt-image-2": {
        "summary": "平台默认主推的电商投放模型，低成本起量、出图稳定，适合商品主图、活动海报、促销 Banner、信息流素材批量生产。",
        "features": (
            "三档质量可选，适合测款快速铺量，也能兼顾高质量成片",
            "覆盖主流横版、竖版、方图比例，适配主图、详情页、Banner 与社媒投放素材",
            "支持 png / jpeg / webp 输出，方便上架、投放和二次设计复用",
        ),
    }
}
DEFAULT_MODEL_RECOMMENDATION_BY_TASK_TYPE = {
    "text_to_image": {
        "summary": "平台默认推荐的文生图投放首选，低成本起量、出图稳定，适合商品主图、活动海报、促销 Banner、种草图等电商投放素材生产。",
        "features": MODEL_PROFILE_BY_ID["gpt-image-2"]["features"],
    },
    "image_to_image": {
        "summary": "平台默认推荐的改图投放首选，重绘稳定、风格统一，适合商品精修、换背景、卖点强化、营销图翻新等电商投放场景。",
        "features": MODEL_PROFILE_BY_ID["gpt-image-2"]["features"],
    },
}
POLL_CONFIG = {
    "text_to_image": {"interval": 5, "max_wait": 600},
    "image_to_image": {"interval": 5, "max_wait": 600},
}

APP_ID = "webAgent"
APP_KEY = "32jdskjdk320eew"
