from __future__ import annotations

from urllib.parse import urlencode

DEFAULT_SEARCH_LOCATION = "uk"
DEFAULT_SEARCH_CATEGORY = "all"


def _join_values(values: list[str] | None) -> str | None:
    if not values:
        return None
    cleaned = [value.strip() for value in values if value.strip()]
    if not cleaned:
        return None
    return ",".join(cleaned)


def build_search_url(
    keyword: str,
    search_location: str = DEFAULT_SEARCH_LOCATION,
    search_category: str = DEFAULT_SEARCH_CATEGORY,
    sort: str | None = None,
    distance: int | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    conditions: list[str] | None = None,
    seller_types: list[str] | None = None,
    mobile_storage_capacity: str | None = None,
    common_for_sale_colour: str | None = None,
    mobile_model_apple: str | None = None,
) -> str:
    params: dict[str, str | int] = {
        "search_category": search_category,
        "q": keyword,
        "search_term_populated_by": "input",
        "keyword_correction": "suggest",
        "search_location": search_location,
    }
    optional_params: dict[str, str | int | None] = {
        "sort": sort,
        "distance": distance,
        "min_price": min_price,
        "max_price": max_price,
        "common_for_sale_condition": _join_values(conditions),
        "seller_type": _join_values(seller_types),
        "mobile_storage_capacity": mobile_storage_capacity,
        "common_for_sale_colour": common_for_sale_colour,
        "mobile_model_apple": mobile_model_apple,
    }
    for key, value in optional_params.items():
        if value not in (None, ""):
            params[key] = value

    params = urlencode(params)
    return f"https://www.gumtree.com/search?{params}"


def build_home_url() -> str:
    return "https://www.gumtree.com/"


def build_favourites_url() -> str:
    return "https://www.gumtree.com/my-account/favourites"


def build_category_suggest_url(keyword: str) -> str:
    params = urlencode({"input": keyword})
    return f"https://my.gumtree.com/api/category/suggest?{params}"


def build_post_ad_create_url(category_id: int) -> str:
    return f"https://www.gumtree.com/postad/create?categoryId={category_id}"


def build_messages_url(conversation_id: str | None = None, open_chat: bool = True) -> str:
    params: dict[str, str] = {}
    if conversation_id:
        params["conversationId"] = conversation_id
    if open_chat:
        params["openChat"] = "true"
    if not params:
        return "https://www.gumtree.com/manage/messages"
    return f"https://www.gumtree.com/manage/messages?{urlencode(params)}"
