from __future__ import annotations

from typing import Any, Dict, Optional

from app.core import state
from app.services.provider_factory import get_provider, canonical_name


def init_provider(name: str) -> Dict[str, Any]:
    provider = get_provider(name)
    metadata = provider.init_metadata()
    existing = state.read_state(provider.name)
    existing.update(metadata)
    state.write_state(provider.name, existing)
    return metadata


def get_cached_state(name: str) -> Dict[str, Any]:
    return state.read_state(canonical_name(name))


def update_state(name: str, data: Dict[str, Any]) -> None:
    state.write_state(canonical_name(name), data)


def list_products(name: str):
    provider = get_provider(name)
    products = provider.list_products()
    cached = get_cached_state(name)
    cached["products"] = [
        {
            "id": str(
                item.get("id")
                or item.get("groupId")
                or item.get("productProfileId")
                or item.get("skuId")
                or item.get("productId")
                or item.get("skuPartNumber")
            ),
            "name": item.get("name") or item.get("groupName") or item.get("skuPartNumber"),
            "raw": item,
        }
        for item in products
    ]
    update_state(name, cached)
    return cached["products"]


def create_user(name: str, identifier: str, product: Optional[str] = None, **kwargs):
    provider = get_provider(name)
    return provider.create_user(identifier, product, **kwargs)


def assign_product(name: str, identifier: str, product: str):
    provider = get_provider(name)
    return provider.assign_product(identifier, product)


def reset_password(name: str, identifier: str, **kwargs):
    provider = get_provider(name)
    return provider.reset_password(identifier, **kwargs)


def delete_user(name: str, identifier: str):
    provider = get_provider(name)
    return provider.delete_user(identifier)


def describe_user(name: str, identifier: str):
    provider = get_provider(name)
    return provider.describe_user(identifier)


def get_aliases(name: str) -> Dict[str, str]:
    return get_cached_state(name).get("aliases", {})


def set_alias(name: str, alias: str, product_id: str) -> Dict[str, str]:
    alias = alias.lower()
    data = get_cached_state(name)
    aliases = data.get("aliases", {})
    aliases[alias] = str(product_id)
    data["aliases"] = aliases
    update_state(name, data)
    return aliases


def remove_alias(name: str, alias: str) -> Dict[str, str]:
    alias = alias.lower()
    data = get_cached_state(name)
    aliases = data.get("aliases", {})
    if alias in aliases:
        aliases.pop(alias)
        data["aliases"] = aliases
        update_state(name, data)
    return aliases


def run_self_test(name: str, product: Optional[str] = None):
    provider = get_provider(name)
    return provider.self_test(product_id=product)
