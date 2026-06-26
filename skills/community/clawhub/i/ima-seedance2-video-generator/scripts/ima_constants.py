"""
IMA Video Generation Constants
Version: 1.0.0 (Production Environment Only)

This build is configured for PRODUCTION ENVIRONMENT ONLY.
Test environment is not supported in this build.

Central configuration and constants for Seedance 2.0 video generation.
Includes:
- API endpoint URLs (production only)
- Model definitions and mappings
- Polling and timeout settings
- Upload authentication keys
"""

from pathlib import Path

# ─── API Endpoints (Production Environment Only) ─────────────────────────────

# Production environment base URLs (hardcoded)
DEFAULT_BASE_URL    = "https://api.imastudio.com"
DEFAULT_IM_BASE_URL = "https://imapi.liveme.com"

BASE_URL    = DEFAULT_BASE_URL
IM_BASE_URL = DEFAULT_IM_BASE_URL

# ─── Local Paths ──────────────────────────────────────────────────────────────

PREFS_PATH = str(Path.home() / ".openclaw" / "memory" / "ima_prefs.json")
MAX_POLL_WAIT_SECONDS = 40 * 60  # 40 minutes
VIDEO_RECORDS_URL = "https://www.imastudio.com/ai-creation/text-to-video"

# ─── Poll Configuration ───────────────────────────────────────────────────────

# Poll interval (seconds) and max wait (seconds) per task type
POLL_CONFIG = {
    "text_to_video":             {"interval": 8,  "max_wait": MAX_POLL_WAIT_SECONDS},
    "image_to_video":            {"interval": 8,  "max_wait": MAX_POLL_WAIT_SECONDS},
    "first_last_frame_to_video": {"interval": 8,  "max_wait": MAX_POLL_WAIT_SECONDS},
    "reference_image_to_video":  {"interval": 8,  "max_wait": MAX_POLL_WAIT_SECONDS},
}

# ─── Upload Authentication ────────────────────────────────────────────────────

# App Key configuration (for OSS upload authentication)
# These are shared keys used by all IMA skill-based uploads
# NOT a secret - visible in public source code
# Used to generate request signatures for imapi.liveme.com upload API
# See SECURITY.md § "Credentials" for security implications
APP_ID = "webAgent"
APP_KEY = "32jdskjdk320eew"
#APP_KEY = "275c6a57"

# ─── Model Configuration ──────────────────────────────────────────────────────

# Model allowlist for ima-seedance2-video-generator skill (canonical IDs)
CANONICAL_MODEL_IDS = {"ima-pro", "ima-pro-fast"}

# User-friendly aliases
MODEL_ID_ALIASES = {
    "seedance 2.0": "ima-pro",
    "seedance": "ima-pro",
    "ima_pro": "ima-pro",
    "pro": "ima-pro",
    "专业版": "ima-pro",
    "高质量": "ima-pro",
    "seedance 2.0 fast": "ima-pro-fast",
    "seedance fast": "ima-pro-fast",
    "ima_pro_fast": "ima-pro-fast",
    "fast": "ima-pro-fast",
    "极速": "ima-pro-fast",
    "快速": "ima-pro-fast",
}

ALLOWED_MODEL_IDS = CANONICAL_MODEL_IDS

# ─── Asset Compliance Verification ───────────────────────────────────────────

# Asset types supported for compliance verification
ASSET_TYPES = {
    "image": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"],
    "video": [".mp4", ".webm", ".mov", ".avi", ".mkv", ".flv"],
    "audio": [".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"]
}

# Task types that require asset compliance verification
COMPLIANCE_REQUIRED_TASK_TYPES = {
    "image_to_video",
    "first_last_frame_to_video",
    "reference_image_to_video"
}

# Verification status codes
VERIFICATION_STATUS = {
    "SUCCESS": "success",
    "FAILED": "failed",
    "PROCESSING": "processing"
}

# ─── Model Name Mapping ───────────────────────────────────────────────────────

def normalize_model_id(model_id: str | None) -> str | None:
    """Normalize user input model IDs into canonical skill-facing IDs."""
    if not model_id:
        return None
    normalized = model_id.strip().lower()
    if normalized in CANONICAL_MODEL_IDS:
        return normalized
    return MODEL_ID_ALIASES.get(normalized, model_id)


def to_user_facing_model_name(model_name: str | None, model_id: str | None) -> str:
    """Return Seedance-branded model name for user-visible messaging."""
    canonical = normalize_model_id(model_id)
    if canonical == "ima-pro":
        return "Seedance 2.0"
    if canonical == "ima-pro-fast":
        return "Seedance 2.0 Fast"
    return model_name or "Seedance"
