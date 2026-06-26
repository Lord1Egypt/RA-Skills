from errors import ValidationError


def normalize_trade_symbol(symbol: str) -> str:
    s = (symbol or "").strip().upper()
    if not s:
        raise ValidationError("symbol is required", hint="请传入证券代码，例如 HK.00700 或 US.AAPL")

    if s.startswith("HK-"):
        return s.replace("-", ".", 1)
    if s.startswith("US-"):
        return s.replace("-", ".", 1)

    if s.startswith("HK.") or s.startswith("US."):
        return s

    if s.isdigit() and len(s) <= 5:
        return f"HK.{s.zfill(5)}"

    raise ValidationError(
        f"unsupported symbol format: {symbol}",
        hint="当前请使用 HK.00700、HK-00700、US.AAPL 这类格式",
    )
