"""
Canonical model families.

Different integrations log the same logical model under different strings:

    OpenAI-wrap         "claude-sonnet-4.6"          (dot form, from provider header)
    Anthropic-wrap      "claude-sonnet-4-6"          (hyphen form, from API)
    OpenClaw            "claude-haiku-4-5-20251001"  (pinned snapshot)
    OpenRouter          "anthropic/claude-sonnet-4.6"(prefixed form)

We want reports to group these as one row. `canonical_family(name)` returns
a stable slug that collapses these variants.

Rules:
    - lowercase
    - strip provider prefix (`anthropic/`, `openai/`, `google/`, `openrouter/`)
      but preserve `openrouter/` as a standalone tag — OpenRouter routing
      is itself a billing distinction, so we canonicalize to `openrouter/<family>`.
    - dots → hyphens (Anthropic/OpenAI variance)
    - strip date-pinned suffix: `-20251001` / `-2025-09-29` / `-latest`
    - strip fine-tune / thinking suffixes: `:thinking`, `@001`, `-hd`
"""
from __future__ import annotations

import re


_DATE_SUFFIX = re.compile(r"-(?:\d{8}|\d{4}-\d{2}-\d{2}|latest|stable)$")
_TAG_SUFFIX = re.compile(r"(?:[:@][\w\d-]+|-hd|-fast)$")
_STRIP_PREFIXES = ("anthropic/", "openai/", "google/", "gemini/",
                   "mistral/", "cohere/", "deepseek/", "meta/",
                   "meta-llama/", "together/", "fireworks/", "groq/",
                   "perplexity/", "xai/", "vertex_ai/")


def canonical_family(name: str) -> str:
    if not name:
        return name
    slug = name.strip().lower()

    # Preserve openrouter/ as a billing-distinct route, but canonicalize
    # whatever follows it.
    openrouter = False
    if slug.startswith("openrouter/"):
        openrouter = True
        slug = slug[len("openrouter/"):]

    # Strip other provider prefixes.
    for pre in _STRIP_PREFIXES:
        if slug.startswith(pre):
            slug = slug[len(pre):]
            break

    # Dots -> hyphens.
    slug = slug.replace(".", "-")

    # Strip common tag suffixes (thinking, @001, -hd) before date.
    prev = None
    while prev != slug:
        prev = slug
        slug = _TAG_SUFFIX.sub("", slug)

    # Strip date-pinned suffix (one pass is enough).
    slug = _DATE_SUFFIX.sub("", slug)

    return f"openrouter/{slug}" if openrouter else slug


def same_family(a: str, b: str) -> bool:
    return canonical_family(a) == canonical_family(b)
