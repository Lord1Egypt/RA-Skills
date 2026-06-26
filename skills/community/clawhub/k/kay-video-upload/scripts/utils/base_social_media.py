"""
base_social_media.py - 自包含版，不依赖外部 conf
"""
from pathlib import Path
from typing import List

# BASE_DIR 指向 scripts/ 目录
BASE_DIR = Path(__file__).parent.parent

SOCIAL_MEDIA_DOUYIN = "douyin"
SOCIAL_MEDIA_TENCENT = "tencent"
SOCIAL_MEDIA_TIKTOK = "tiktok"
SOCIAL_MEDIA_BILIBILI = "bilibili"
SOCIAL_MEDIA_KUAISHOU = "kuaishou"


def get_supported_social_media() -> List[str]:
    return [SOCIAL_MEDIA_DOUYIN, SOCIAL_MEDIA_TENCENT, SOCIAL_MEDIA_TIKTOK, SOCIAL_MEDIA_KUAISHOU]


def get_cli_action() -> List[str]:
    return ["upload", "login", "watch"]


async def set_init_script(context):
    stealth_js_path = BASE_DIR / "utils" / "stealth.min.js"
    if stealth_js_path.exists():
        await context.add_init_script(path=str(stealth_js_path))
    return context
