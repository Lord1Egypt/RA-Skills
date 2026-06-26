from __future__ import annotations

import os

DEFAULT_BASE_URL = os.getenv("IMA_BASE_URL", "https://api.imastudio.com")
DEFAULT_IM_BASE_URL = os.getenv("IMA_IM_BASE_URL", "https://imapi.liveme.com")

PREFS_PATH = os.path.expanduser("~/.openclaw/memory/ima_prefs.json")
VIDEO_MAX_WAIT_SECONDS = 40 * 60
VIDEO_RECORDS_URL = "https://www.imastudio.com/ai-creation/text-to-video"

VIDEO_TASK_TYPES = (
    "text_to_video",
    "image_to_video",
    "first_last_frame_to_video",
    "reference_image_to_video",
)

POLL_CONFIG = {
    "text_to_video": {"interval": 8, "max_wait": VIDEO_MAX_WAIT_SECONDS},
    "image_to_video": {"interval": 8, "max_wait": VIDEO_MAX_WAIT_SECONDS},
    "first_last_frame_to_video": {"interval": 8, "max_wait": VIDEO_MAX_WAIT_SECONDS},
    "reference_image_to_video": {"interval": 8, "max_wait": VIDEO_MAX_WAIT_SECONDS},
}

APP_ID = "webAgent"
APP_KEY = "32jdskjdk320eew"
