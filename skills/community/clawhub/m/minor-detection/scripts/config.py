# 模块说明：
# - bundled skill 内部运行时配置。
# - 只给 skill 自己的脚本使用。

from __future__ import annotations

import os
from typing import Dict


def _env(name: str, default: str = "") -> str:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip()


def _env_int(name: str, default: int) -> int:
    raw = _env(name, "")
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_float(name: str, default: float) -> float:
    raw = _env(name, "")
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


CLASSIFIER_BASE_URL = _env("MINOR_DETECTION_CLASSIFIER_BASE_URL")
CLASSIFIER_API_KEY = _env("MINOR_DETECTION_CLASSIFIER_API_KEY")
CLASSIFIER_MODEL = _env("MINOR_DETECTION_CLASSIFIER_MODEL") or "gemini-2.5-flash-lite"
CLASSIFIER_TIMEOUT_SEC = _env_int("MINOR_DETECTION_CLASSIFIER_TIMEOUT_SEC", 120)
CLASSIFIER_MAX_RETRIES = _env_int("MINOR_DETECTION_CLASSIFIER_MAX_RETRIES", 2)
CLASSIFIER_RETRY_BACKOFF_SEC = _env_float("MINOR_DETECTION_CLASSIFIER_RETRY_BACKOFF_SEC", 2.0)

EMBEDDING_BASE_URL = _env("MINOR_DETECTION_EMBEDDING_BASE_URL")
EMBEDDING_API_KEY = _env("MINOR_DETECTION_EMBEDDING_API_KEY")
EMBEDDING_MODEL = _env("MINOR_DETECTION_EMBEDDING_MODEL") or "text-embedding-3-small"

PIPELINE_TIMEZONE = _env("MINOR_DETECTION_TIMEZONE") or "Asia/Shanghai"
RETRIEVAL_TOP_K = _env_int("MINOR_DETECTION_RETRIEVAL_TOP_K", 3)

LOW_CONFIDENCE_THRESHOLD = 0.34
HIGH_CONFIDENCE_THRESHOLD = 0.67


def export_embedding_env() -> Dict[str, str]:
    env = {
        "SKILL_EMBEDDING_BASE_URL": EMBEDDING_BASE_URL,
        "SKILL_EMBEDDING_API_KEY": EMBEDDING_API_KEY,
        "SKILL_EMBEDDING_MODEL": EMBEDDING_MODEL,
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUTF8": "1",
    }
    return {key: value for key, value in env.items() if value}


def classifier_runtime_snapshot() -> Dict[str, object]:
    return {
        "base_url": CLASSIFIER_BASE_URL,
        "model": CLASSIFIER_MODEL,
        "api_key_present": bool(CLASSIFIER_API_KEY),
        "timeout_sec": CLASSIFIER_TIMEOUT_SEC,
        "max_retries": CLASSIFIER_MAX_RETRIES,
        "retry_backoff_sec": CLASSIFIER_RETRY_BACKOFF_SEC,
    }


def embedding_runtime_snapshot() -> Dict[str, object]:
    return {
        "base_url": EMBEDDING_BASE_URL,
        "model": EMBEDDING_MODEL,
        "api_key_present": bool(EMBEDDING_API_KEY),
        "top_k": RETRIEVAL_TOP_K,
    }
