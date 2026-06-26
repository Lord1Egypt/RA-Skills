from __future__ import annotations

from functools import lru_cache
from typing import Dict

from app.core.config import get_provider_config
from app.providers.adobe.provider import AdobeProvider
from app.providers.office365.provider import Office365Provider

PROVIDER_ALIASES = {
    "office365": "office365",
    "o365": "office365",
    "m365": "office365",
    "adobe": "adobe",
    "ps": "adobe",
    "photoshop": "adobe",
}


def canonical_name(name: str) -> str:
    key = PROVIDER_ALIASES.get(name.lower())
    if not key:
        raise ValueError(f"未知 provider: {name}")
    return key


@lru_cache(maxsize=4)
def get_provider(name: str):
    key = canonical_name(name)

    config = get_provider_config(key)

    if key == "office365":
        return Office365Provider(config)
    if key == "adobe":
        return AdobeProvider(config)

    raise ValueError(f"未实现 provider: {name}")
