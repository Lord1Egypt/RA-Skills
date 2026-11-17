#!/usr/bin/env python3
"""
LLM Tagging + Library Split module for Apparel Keyword Expert.
Uses the finalized System Prompt + Few-shot + User template.
"""

import json
import os
from typing import List, Dict, Any, Optional, Callable

try:
    from prompts.apparel_tagging import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
except ImportError:
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from prompts.apparel_tagging import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


VALID_PRIMARY_TYPES = {
    "Core Product", "Dress Length", "Neckline", "Sleeve Type", "Silhouette", "Fit",
    "Occasion", "Pattern", "Material", "Size Type", "Color", "Style", "Closure Type",
    "Care", "Feature", "Selling Point", "Scenario", "Audience", "Specification",
    "Question", "Brand", "Competitor", "Other"
}

VALID_LIBRARIES = {"positive", "negative", "review"}
VALID_RELEVANCE = {"high", "medium", "low", "irrelevant"}


def default_llm_call(system: str, user: str, model: Optional[str] = None) -> str:
    """
    Default LLM caller using OpenAI-compatible API (xAI / OpenAI / any compatible endpoint).

    Environment variables (in priority order):
      XAI_API_KEY / OPENAI_API_KEY / LLM_API_KEY  → API key
      LLM_BASE_URL                                 → base URL (default https://api.x.ai/v1)
      LLM_MODEL                                    → model name (default grok-4.5 / grok-3)

    Raises RuntimeError if no key is found or the call fails.
    """
    api_key = (
        os.getenv("XAI_API_KEY")
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("LLM_API_KEY")
    )
    if not api_key:
        raise RuntimeError(
            "No LLM API key found. Set XAI_API_KEY / OPENAI_API_KEY / LLM_API_KEY"
        )

    base_url = os.getenv("LLM_BASE_URL", "https://api.x.ai/v1")
    model_name = model or os.getenv("LLM_MODEL", "grok-4.5")

    try:
        from openai import OpenAI
    except ImportError as e:
        raise RuntimeError(
            "openai package required for default_llm_call. pip install openai"
        ) from e

    client = OpenAI(api_key=api_key, base_url=base_url)

    # Prefer JSON mode when supported
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.15,
    }
    try:
        kwargs["response_format"] = {"type": "json_object"}
        resp = client.chat.completions.create(**kwargs)
    except Exception:
        # Fallback without response_format
        kwargs.pop("response_format", None)
        resp = client.chat.completions.create(**kwargs)

    content = resp.choices[0].message.content
    if not content:
        raise RuntimeError("Empty response from LLM")
    return content.strip()


def batch_list(items: List[str], batch_size: int = 100) -> List[List[str]]:
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]


def build_user_prompt(seed: str, product_context: str, keywords: List[str]) -> str:
    keyword_list = "\n".join(f"{i+1}. {kw}" for i, kw in enumerate(keywords))
    return USER_PROMPT_TEMPLATE.format(
        product_context=product_context or "Not provided",
        seed=seed,
        n=len(keywords),
        keyword_list=keyword_list
    )


def validate_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Basic validation and safe defaults for simplified schema."""
    if item.get("primary_type") not in VALID_PRIMARY_TYPES:
        item["primary_type"] = "Other"
        # Do NOT change library based on invalid primary_type — library is determined
        # by rule pre-filter or LLM coarse split, not by primary_type validity
        item["confidence"] = min(float(item.get("confidence", 0.5)), 0.5)

    if item.get("library") not in VALID_LIBRARIES:
        item["library"] = "review"

    if item.get("relevance") not in VALID_RELEVANCE:
        item["relevance"] = "medium"

    if not isinstance(item.get("secondary_types"), list):
        item["secondary_types"] = []
    if not isinstance(item.get("attribute_categories"), list):
        item["attribute_categories"] = []
    if not isinstance(item.get("suggested_positions"), list):
        item["suggested_positions"] = []

    item["is_complete_attribute_phrase"] = bool(item.get("is_complete_attribute_phrase", False))
    try:
        item["confidence"] = float(item.get("confidence", 0.7))
    except (TypeError, ValueError):
        item["confidence"] = 0.7

    # Backward compat: ensure removed fields exist as defaults
    item.setdefault("normalized", item.get("keyword", ""))
    item.setdefault("amazon_facet_mapping", [])
    item.setdefault("relevance_reason", "")
    item.setdefault("notes", "")

    return item


def llm_tag_and_split(
    keywords: List[str],
    seed: str,
    product_context: Optional[str] = None,
    batch_size: int = 100,
    llm_call_fn: Optional[Callable[[str, str], str]] = None,
) -> Dict[str, Any]:
    """
    Main entry for LLM tagging + library split.

    Parameters
    ----------
    keywords : list of str
        Deduplicated keywords from mining stage.
    seed : str
        Original seed keyword.
    product_context : str, optional
        Product description for better relevance judgment.
    batch_size : int
        Keywords per LLM call (recommended 40-70).
    llm_call_fn : callable, optional
        Function that accepts (system_prompt, user_prompt) and returns raw JSON string.
        If None, uses default_llm_call (OpenAI-compatible / xAI via env keys).

    Returns
    -------
    dict with keys:
        results, positive, negative, review, summary
    """
    all_results = []

    if not keywords:
        return {
            "results": [],
            "positive": [],
            "negative": [],
            "review": [],
            "summary": {
                "positive_count": 0,
                "negative_count": 0,
                "review_count": 0,
                "high_relevance_count": 0,
                "complete_attribute_phrase_count": 0,
            },
        }

    # Resolve the actual caller: explicit > default_llm_call
    caller = llm_call_fn if llm_call_fn is not None else default_llm_call

    for batch in batch_list(keywords, batch_size):
        user_prompt = build_user_prompt(seed, product_context, batch)

        raw = None
        last_err = None
        for attempt in range(2):  # one retry on JSON / call failure
            try:
                raw = caller(SYSTEM_PROMPT, user_prompt)
                parsed = json.loads(raw)
                for item in parsed.get("results", []):
                    all_results.append(validate_item(item))
                last_err = None
                break
            except Exception as e:
                last_err = e
                continue

        if last_err is not None:
            # Both attempts failed → push batch into review
            for kw in batch:
                all_results.append(validate_item({
                    "keyword": kw,
                    "normalized": kw,
                    "primary_type": "Other",
                    "secondary_types": [],
                    "attribute_categories": [],
                    "is_complete_attribute_phrase": False,
                    "amazon_facet_mapping": [],
                    "relevance": "medium",
                    "relevance_reason": f"LLM call or parse failed: {str(last_err)[:100]}",
                    "library": "review",
                    "suggested_positions": [],
                    "confidence": 0.2,
                    "notes": "error",
                }))

    positive = [r for r in all_results if r.get("library") == "positive"]
    negative = [r for r in all_results if r.get("library") == "negative"]
    review = [r for r in all_results if r.get("library") == "review"]

    summary = {
        "positive_count": len(positive),
        "negative_count": len(negative),
        "review_count": len(review),
        "high_relevance_count": sum(1 for r in all_results if r.get("relevance") == "high"),
        "complete_attribute_phrase_count": sum(
            1 for r in all_results if r.get("is_complete_attribute_phrase")
        ),
    }

    return {
        "results": all_results,
        "positive": positive,
        "negative": negative,
        "review": review,
        "summary": summary,
    }


if __name__ == "__main__":
    # Quick smoke test (placeholder mode)
    demo = llm_tag_and_split(
        keywords=["above the knee dress", "zara summer dress", "midi dress for women"],
        seed="summer dress",
        product_context="Women's casual summer dresses, lightweight, midi or above the knee",
    )
    print(json.dumps(demo["summary"], indent=2, ensure_ascii=False))
