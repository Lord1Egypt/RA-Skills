"""Pricing registry for scripts."""

from typing import Optional

USD_TO_INR = 83.0  # Conversion rate as of July 10 2025

PRICING = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-32k": {"input": 0.06, "output": 0.12},
    "dbrx-instruct": {"input": 0.001, "output": 0.002},
    "dbrx-base": {"input": 0.001, "output": 0.002},
    "dolly-v2-12b": {"input": 0.001, "output": 0.002},
    "dolly-v2-7b": {"input": 0.001, "output": 0.002},
    "dolly-v2-3b": {"input": 0.001, "output": 0.002},
    "voyage-2": {"input": 0.0001, "output": 0.0001},
    "voyage-large-2": {"input": 0.0001, "output": 0.0001},
    "voyage-code-2": {"input": 0.0001, "output": 0.0001},
    "voyage-finance-2": {"input": 0.0001, "output": 0.0001},
    "voyage-law-2": {"input": 0.0001, "output": 0.0001},
    "voyage-multilingual-2": {"input": 0.0001, "output": 0.0001},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
    "gpt-3.5-turbo-16k": {"input": 0.003, "output": 0.004},
    "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
    "claude-3-sonnet-20240229": {"input": 0.003, "output": 0.015},
    "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125},
    "claude-3.5-sonnet-20240620": {"input": 0.003, "output": 0.015},
    "claude-3.5-sonnet-20241022": {"input": 0.003, "output": 0.015},
    "claude-3.5-haiku-20241022": {"input": 0.001, "output": 0.005},
    "claude-3-5-sonnet-20240620": {"input": 0.003, "output": 0.015},
}


def get_pricing_rate(model: str, input_tokens: bool) -> Optional[float]:
    pricing = PRICING.get(model)
    if not pricing:
        return None
    return pricing["input" if input_tokens else "output"]
