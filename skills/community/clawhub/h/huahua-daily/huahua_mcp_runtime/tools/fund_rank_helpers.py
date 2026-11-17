"""Shared validation and response shaping for fund rank tools."""


async def get_batch_period_ranks(codes, *, validate_code, post) -> dict:
    if len(codes) > 50:
        raise ValueError("codes 最多支持 50 只基金")
    validated_codes = []
    seen = set()
    for code in codes:
        normalized = validate_code(code)
        if normalized not in seen:
            validated_codes.append(normalized)
            seen.add(normalized)
    if not validated_codes:
        return {
            "data": {},
            "requestedCodes": [],
            "missingCodes": [],
            "complete": True,
        }
    payload = await post("/api/fund/period-rank/batch", {"codes": validated_codes})
    data = payload.get("data") if isinstance(payload, dict) else None
    data = data if isinstance(data, dict) else {}
    missing_codes = [code for code in validated_codes if code not in data]
    return {
        "data": data,
        "requestedCodes": validated_codes,
        "missingCodes": missing_codes,
        "complete": not missing_codes,
    }
