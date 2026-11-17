"""Strict history transport shared by fund tools."""


async def search_fund(getter, query: str) -> list:
    normalized = str(query or "").strip()
    if not normalized:
        raise ValueError("搜索关键词不能为空")
    if len(normalized) > 100:
        raise ValueError("搜索关键词过长，最多 100 字符")
    data = await getter("/api/search", params={"key": normalized})
    return data if isinstance(data, list) else []


async def get_strict_item_history(getter, validator, code: str) -> list:
    validated_code = validator(code)
    data = await getter(
        f"/api/history/{validated_code}",
        params={"strictFreshness": True},
    )
    return data if isinstance(data, list) else []
