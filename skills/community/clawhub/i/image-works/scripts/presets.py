"""
Platform preset templates for image-works.
Maps preset names to operation sequences for Chinese social platforms.
"""
from typing import List, Dict

PRESETS = {
    "wechat-moments": {
        "name": "微信朋友圈 9宫格",
        "description": "Cut image into 3×3 grid for WeChat Moments",
        "operations": [
            {"type": "resize", "width": 1080, "height": 1080, "fit": "cover"},
            {"type": "compress", "quality": 80},
        ],
        "notes": "Run once per image; use a grid cutter tool for 9-grid split",
    },
    "wechat-cover": {
        "name": "微信公众号封面图",
        "description": "WeChat Official Account cover: 900×383, <10MB",
        "operations": [
            {"type": "resize", "width": 900, "height": 383, "fit": "cover"},
            {"type": "compress", "quality": 85},
        ],
    },
    "xiaohongshu": {
        "name": "小红书笔记图片",
        "description": "Xiaohongshu note image: 3:4 ratio, 1080×1440",
        "operations": [
            {"type": "crop", "aspect_ratio": "3:4"},
            {"type": "resize", "width": 1080, "height": 1440, "fit": "cover"},
            {"type": "compress", "quality": 85},
        ],
    },
    "taobao-main": {
        "name": "淘宝主图",
        "description": "Taobao main image: 800×800 1:1, <500KB",
        "operations": [
            {"type": "resize", "width": 800, "height": 800, "fit": "cover"},
            {"type": "compress", "quality": 80, "target_size_kb": 500},
        ],
    },
    "douyin-cover": {
        "name": "抖音视频封面",
        "description": "Douyin video cover: 1920×1080 16:9",
        "operations": [
            {"type": "resize", "width": 1920, "height": 1080, "fit": "cover"},
            {"type": "compress", "quality": 85},
        ],
    },
    "weibo": {
        "name": "微博配图",
        "description": "Weibo image: 1200px wide, <20MB",
        "operations": [
            {"type": "resize", "width": 1200, "fit": "inside"},
            {"type": "compress", "quality": 85},
        ],
    },
    "bilibili-cover": {
        "name": "B站专栏封面",
        "description": "Bilibili cover: 16:9, 1920×1080 recommended",
        "operations": [
            {"type": "crop", "aspect_ratio": "16:9"},
            {"type": "resize", "width": 1920, "height": 1080, "fit": "cover"},
            {"type": "compress", "quality": 90},
        ],
    },
    "avatar": {
        "name": "通用头像",
        "description": "Avatar: 400×400 1:1, <200KB",
        "operations": [
            {"type": "resize", "width": 400, "height": 400, "fit": "cover"},
            {"type": "compress", "quality": 85, "target_size_kb": 200},
        ],
    },
}

# User presets file path
USER_PRESETS_PATH = "~/.openclaw/data/image-works/presets.json"


def get_preset(name: str) -> Dict:
    """Get a preset configuration by name."""
    preset = PRESETS.get(name)
    if not preset:
        return {"error": f"Preset '{name}' not found. Available: {', '.join(PRESETS.keys())}"}
    return preset


def list_presets() -> Dict:
    """List all available presets with descriptions."""
    return {k: {"name": v["name"], "description": v["description"]}
            for k, v in PRESETS.items()}


def resolve_preset(name: str) -> List[Dict]:
    """Resolve a preset name to a list of operations."""
    preset = PRESETS.get(name)
    if not preset:
        return []
    return preset.get("operations", [])
