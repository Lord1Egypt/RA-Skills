#!/usr/bin/env python3
"""
Regenerate references/pricing.md from LiteLLM + OpenRouter.

Covers every model both aggregators expose across modes: chat, completion,
embedding, image generation/edit, audio transcription/speech, video, rerank,
search, OCR, moderation, realtime, responses.

Each (provider, mode) pair becomes its own markdown section, with the billing
unit encoded in the header so the parser can read it back:

  ## OpenAI — image_generation (per image)
  ## Anthropic — chat (per 1M tokens)

Prices are stored as "per 1M units" regardless of unit — a $0.04/image model
becomes $40,000/1M images. That keeps one number per cell; downstream code
checks `unit` before multiplying.

Usage:
    python3 scripts/refresh_pricing.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _sources  # noqa: E402


OUT_FILE = Path(__file__).resolve().parent.parent / "references" / "pricing.md"
MIN_TOTAL_ROWS = 100

# Chosen billing unit per mode. We look at the cost fields in priority order
# per mode. First hit wins.
#   (input_field, output_field, unit)
# `None` means "not applicable for this side" (e.g. embeddings have no output).
MODE_UNITS = {
    "chat":                 [("input_cost_per_token", "output_cost_per_token", "token")],
    "completion":           [("input_cost_per_token", "output_cost_per_token", "token")],
    "responses":            [("input_cost_per_token", "output_cost_per_token", "token")],
    "embedding":            [("input_cost_per_token", "output_cost_per_token", "token")],
    "moderation":           [("input_cost_per_token", "output_cost_per_token", "token")],
    "unspecified":          [("input_cost_per_token", "output_cost_per_token", "token")],
    "realtime":             [("input_cost_per_token", "output_cost_per_token", "token")],
    "image_generation":     [("input_cost_per_image", "output_cost_per_image", "image")],
    "image_edit":           [("input_cost_per_image", "output_cost_per_image", "image")],
    "audio_transcription":  [("input_cost_per_second", "output_cost_per_second", "second")],
    "audio_speech":         [("input_cost_per_token", "output_cost_per_second", "token"),
                             ("input_cost_per_character", "output_cost_per_second", "character")],
    "video_generation":     [("input_cost_per_second", "output_cost_per_second", "second")],
    "rerank":               [("input_cost_per_query", None, "query")],
    "search":               [("input_cost_per_query", None, "query")],
    "vector_store":         [("input_cost_per_query", None, "query")],
    "ocr":                  [("ocr_cost_per_page", None, "page")],
}

PROVIDER_DISPLAY = {
    "anthropic": "Anthropic",
    "openai": "OpenAI",
    "text-completion-openai": "OpenAI",
    "google": "Google",
    "gemini": "Google",
    "vertex_ai-language-models": "Google (Vertex)",
    "vertex_ai-anthropic_models": "Google (Vertex Anthropic)",
    "vertex_ai-mistral_models": "Google (Vertex Mistral)",
    "vertex_ai-meta_models": "Google (Vertex Meta)",
    "vertex_ai-ai21_models": "Google (Vertex AI21)",
    "vertex_ai-image-models": "Google (Vertex)",
    "vertex_ai-embedding-models": "Google (Vertex)",
    "vertex_ai-chat-models": "Google (Vertex)",
    "vertex_ai-code-chat-models": "Google (Vertex)",
    "vertex_ai-code-text-models": "Google (Vertex)",
    "vertex_ai-text-models": "Google (Vertex)",
    "groq": "Groq",
    "mistral": "Mistral",
    "codestral": "Mistral",
    "cohere_chat": "Cohere",
    "cohere": "Cohere",
    "deepseek": "DeepSeek",
    "perplexity": "Perplexity",
    "xai": "xAI",
    "meta_llama": "Meta Llama",
    "together_ai": "Together AI",
    "fireworks_ai": "Fireworks",
    "bedrock": "AWS Bedrock",
    "bedrock_converse": "AWS Bedrock",
    "azure": "Azure OpenAI",
    "azure_ai": "Azure AI",
    "databricks": "Databricks",
    "nebius": "Nebius",
    "cerebras": "Cerebras",
    "sambanova": "SambaNova",
    "watsonx": "IBM watsonx",
    "replicate": "Replicate",
    "ai21": "AI21",
    "anyscale": "Anyscale",
    "deepinfra": "DeepInfra",
    "voyage": "Voyage",
    "jina_ai": "Jina AI",
    "assemblyai": "AssemblyAI",
    "openrouter": "OpenRouter",
    "recraft": "Recraft",
    "luma_ai": "Luma AI",
    "runway": "Runway",
    "bytez": "Bytez",
    "novita": "Novita",
    "infinity": "Infinity",
    "hyperbolic": "Hyperbolic",
    "featherless_ai": "Featherless AI",
    "friendliai": "FriendliAI",
    "lambda_ai": "Lambda AI",
}


def provider_display(key: str) -> str:
    return PROVIDER_DISPLAY.get(key, key.replace("_", " ").title())


def _normalize_cost(entry: dict, field: str) -> float:
    """Return cost * 1M (for token/character fields) or raw (for everything else)."""
    val = entry.get(field)
    if val is None:
        return 0.0
    try:
        val = float(val)
    except (TypeError, ValueError):
        return 0.0
    # Per-token and per-character fields are in per-token units; scale to 1M.
    if "per_token" in field or "per_character" in field:
        return val * 1_000_000
    # Per-image / per-second / per-query / per-page are given per-1, so scale to 1M
    # so every column in pricing.md is "per 1M units" uniformly.
    return val * 1_000_000


def extract_cost(entry: dict, mode: str) -> Optional[tuple]:
    """
    Given a LiteLLM entry and its mode, figure out the primary input/output cost
    and the billing unit. Returns (input_cost_per_1m, output_cost_per_1m, unit)
    or None if we can't price it.
    """
    recipes = MODE_UNITS.get(mode)
    if not recipes:
        # Unknown mode. Try token pricing as a last resort.
        recipes = [("input_cost_per_token", "output_cost_per_token", "token")]

    for recipe in recipes:
        in_field, out_field, unit = recipe
        inp = _normalize_cost(entry, in_field) if in_field else 0.0
        outp = _normalize_cost(entry, out_field) if out_field else 0.0
        # Accept if at least one side has nonzero cost.
        if inp > 0 or outp > 0:
            return (inp, outp, unit)
    return None


def fetch_litellm_rows() -> list:
    """Return [(provider_display, mode, unit, model_id, input_per_1m, output_per_1m)]."""
    ll = _sources.LiteLLMSource()
    data, _ = ll._data()
    if not data:
        return []

    rows = []
    for model_id, entry in data.items():
        if not isinstance(entry, dict) or model_id == "sample_spec":
            continue
        if model_id.startswith("ft:"):
            continue  # fine-tune variants
        mode = entry.get("mode") or "unspecified"
        result = extract_cost(entry, mode)
        if result is None:
            continue
        inp, outp, unit = result
        provider_key = entry.get("litellm_provider") or "unknown"
        rows.append((
            provider_display(provider_key),
            mode,
            unit,
            model_id,
            inp,
            outp,
        ))
    return rows


def fetch_openrouter_rows() -> list:
    """Return [(model_id_with_prefix, input_per_1m, output_per_1m)]. All tokens."""
    orr = _sources.OpenRouterSource()
    data, _ = orr._data()
    if not data:
        return []

    rows = []
    for item in data.get("data", []):
        mid = item.get("id")
        if not mid:
            continue
        pricing = item.get("pricing") or {}
        try:
            inp = float(pricing.get("prompt", 0))
            outp = float(pricing.get("completion", 0))
        except (TypeError, ValueError):
            continue
        if inp <= 0 and outp <= 0:
            continue
        rows.append((f"openrouter/{mid}", inp * 1_000_000, outp * 1_000_000))
    return rows


_UNIT_PLURAL = {
    "token": "tokens",
    "character": "characters",
    "image": "images",
    "second": "seconds",
    "query": "queries",
    "page": "pages",
    "pixel": "pixels",
}


def format_section_header(provider: str, mode: str, unit: str) -> str:
    unit_phrase = f"per 1M {_UNIT_PLURAL.get(unit, unit + 's')}"
    return f"## {provider} — {mode} ({unit_phrase})"


def render(ll_rows: list, or_rows: list) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total = len(ll_rows) + len(or_rows)

    out = [
        "# API Pricing Reference",
        "",
        f"> Auto-generated on {now}.",
        "> Sources: LiteLLM (direct-provider pricing) + OpenRouter (aggregator routing).",
        "> Regenerate with: `python3 scripts/refresh_pricing.py`",
        f"> Total models: {total} ({len(ll_rows)} via LiteLLM, {len(or_rows)} via OpenRouter)",
        "",
        "All prices are USD per 1,000,000 units of the section's billing unit.",
        "So `$3.00` under `per 1M tokens` = $0.000003/token; `$40,000` under",
        "`per 1M images` = $0.04/image.",
        "",
    ]

    # Group LiteLLM rows by (provider, mode, unit)
    sections: dict = {}
    for provider, mode, unit, mid, inp, outp in ll_rows:
        sections.setdefault((provider, mode, unit), []).append((mid, inp, outp))

    for (provider, mode, unit) in sorted(sections):
        entries = sorted(sections[(provider, mode, unit)], key=lambda r: r[0])
        out.append(format_section_header(provider, mode, unit))
        out.append("")
        out.append("| Model | Input | Output |")
        out.append("|-------|-------|--------|")
        for mid, inp, outp in entries:
            out.append(f"| {mid} | ${inp:.4f} | ${outp:.4f} |")
        out.append("")

    if or_rows:
        out.append("## OpenRouter — chat (per 1M tokens)")
        out.append("")
        out.append(
            "OpenRouter-routed pricing. Reflects what you'd pay routing through "
            "OpenRouter (may include markup vs direct-provider)."
        )
        out.append("")
        out.append("| Model | Input | Output |")
        out.append("|-------|-------|--------|")
        for mid, inp, outp in sorted(or_rows):
            out.append(f"| {mid} | ${inp:.4f} | ${outp:.4f} |")
        out.append("")

    out.append("## Token Estimation Rules of Thumb")
    out.append("")
    out.append("- 1 token ~ 4 characters (English)")
    out.append("- 1 token ~ 0.75 words (English)")
    out.append("- 1 page of text ~ 500 tokens")
    out.append("- 1 line of code ~ 10-20 tokens")
    out.append("- JSON/structured output uses ~30% more tokens than plain text")
    out.append("")

    return "\n".join(out)


def main() -> int:
    print("Fetching LiteLLM pricing...", file=sys.stderr)
    ll = fetch_litellm_rows()
    print(f"  {len(ll)} models across {len({(r[0], r[1]) for r in ll})} provider/mode sections", file=sys.stderr)

    print("Fetching OpenRouter pricing...", file=sys.stderr)
    orr = fetch_openrouter_rows()
    print(f"  {len(orr)} routed models", file=sys.stderr)

    total = len(ll) + len(orr)
    if total < MIN_TOTAL_ROWS:
        print(
            f"ERROR: only {total} rows fetched (< {MIN_TOTAL_ROWS}). "
            f"Aborting to preserve existing pricing.md.",
            file=sys.stderr,
        )
        return 1

    OUT_FILE.write_text(render(ll, orr), encoding="utf-8")
    print(f"Wrote {OUT_FILE} ({total} rows)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
