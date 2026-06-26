"""
Unified configuration loader for Office 365 and Adobe providers.
"""
from __future__ import annotations

from typing import Any, Dict

from config import load_config as load_office365_config, load_adobe_config


def load_app_config() -> Dict[str, Dict[str, Any]]:
    """
    Load configuration for all providers from .env.

    Returns:
        dict: {"office365": {...}, "adobe": {...}}
    """
    office_cfg = load_office365_config()
    adobe_cfg = load_adobe_config()
    return {
        "office365": office_cfg,
        "adobe": adobe_cfg,
    }


def get_provider_config(provider: str) -> Dict[str, Any]:
    """
    Helper to fetch configuration for a single provider.

    Args:
        provider: Provider key (office365/adobe/ps).

    Returns:
        dict: Provider-specific configuration dictionary.
    """
    provider = provider.lower()
    config = load_app_config()

    if provider in ("adobe", "ps", "photoshop"):
        return config["adobe"]
    if provider == "office365":
        return config["office365"]

    raise ValueError(f"未知的 provider: {provider}")
