"""
Pricing sources. A source is an object that can answer "what does this model cost?"
given a model name, returning a SourcedPrice or None.

Three sources:
  - LiteLLMSource    : community-maintained aggregator; direct-provider pricing
                        for Anthropic / OpenAI / Google / Groq / Mistral / DeepSeek / etc.
  - OpenRouterSource : live /api/v1/models — use for openrouter/* models
  - StaticMarkdownSource : parses references/pricing.md, offline fallback.

A router in `_pricing.py` picks one per model prefix.

Env vars:
  CW_OFFLINE=1     : never hit the network; serve from cache or static only.
  CW_STATIC_ONLY=1 : skip network sources entirely; used by tests.
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

CACHE_DIR = Path.home() / ".cost-watchdog" / "sources-cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _ttl_from_env() -> int:
    """
    Read CW_PRICE_TTL_SECONDS from the env. Default 24h.
    Set to 0 to force a live fetch on every call.
    """
    raw = os.environ.get("CW_PRICE_TTL_SECONDS")
    if raw is None:
        return 24 * 60 * 60
    try:
        return max(0, int(raw))
    except ValueError:
        return 24 * 60 * 60


DEFAULT_TTL_SECONDS = _ttl_from_env()
HTTP_TIMEOUT = 5.0

LITELLM_URL = (
    "https://raw.githubusercontent.com/BerriAI/litellm/main/"
    "model_prices_and_context_window.json"
)
OPENROUTER_URL = "https://openrouter.ai/api/v1/models"

_PRICING_MD = Path(__file__).resolve().parent.parent / "references" / "pricing.md"
_WS_RE = re.compile(r"\s+")
_PRICE_RE = re.compile(r"\$?\s*([0-9]+(?:\.[0-9]+)?)")


@dataclass(frozen=True)
class SourcedPrice:
    """
    Cost for one model.

    input_per_1m / output_per_1m are priced per 1,000,000 of the unit in `unit`:
      - unit="token":   $ per 1M tokens          (LLM default)
      - unit="image":   $ per 1M images          (e.g. image generation)
      - unit="second":  $ per 1M seconds         (audio / video)
      - unit="query":   $ per 1M queries         (rerank, search)
      - unit="page":    $ per 1M pages           (OCR)
      - unit="character": $ per 1M characters    (legacy text-cost models)

    Callers multiplying by tokens must check `unit == "token"` first.
    """
    input_per_1m: float
    output_per_1m: float
    display_name: str
    provider: str
    source: str          # "litellm" | "openrouter" | "static"
    fetched_at: float    # unix timestamp; 0 for static
    mode: str = "chat"   # chat | embedding | image_generation | image_edit |
                         # audio_transcription | audio_speech | video_generation |
                         # rerank | search | ocr | moderation | realtime | responses
    unit: str = "token"  # see docstring


def canonical_slug(name: str) -> str:
    return _WS_RE.sub("-", name.strip().lower())


def _offline() -> bool:
    return os.environ.get("CW_OFFLINE") == "1"


def _static_only() -> bool:
    return os.environ.get("CW_STATIC_ONLY") == "1"


_BREAKER_STATE: dict = {}  # host -> {"failures": int, "open_until": float}
_BREAKER_THRESHOLD = 3     # consecutive failures that trip the breaker
_BREAKER_COOLDOWN = 60.0   # seconds to stay open before retrying


def _breaker_host(url: str) -> str:
    try:
        from urllib.parse import urlsplit
        return urlsplit(url).netloc
    except Exception:
        return url


def _breaker_should_skip(url: str) -> bool:
    st = _BREAKER_STATE.get(_breaker_host(url))
    if not st:
        return False
    return time.time() < st.get("open_until", 0)


def _breaker_record_failure(url: str) -> None:
    host = _breaker_host(url)
    st = _BREAKER_STATE.setdefault(host, {"failures": 0, "open_until": 0.0})
    st["failures"] += 1
    if st["failures"] >= _BREAKER_THRESHOLD:
        st["open_until"] = time.time() + _BREAKER_COOLDOWN


def _breaker_record_success(url: str) -> None:
    host = _breaker_host(url)
    if host in _BREAKER_STATE:
        _BREAKER_STATE[host] = {"failures": 0, "open_until": 0.0}


def breaker_open(url: str) -> bool:
    """Public: is the breaker currently open for this URL? Used by callers
    that want to surface 'source temporarily skipped' in output."""
    return _breaker_should_skip(url)


def _http_get_json(url: str, timeout: float = HTTP_TIMEOUT) -> Optional[dict]:
    if _offline() or _static_only():
        return None
    if _breaker_should_skip(url):
        return None
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "cost-watchdog/1.0"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.load(resp)
        _breaker_record_success(url)
        return data
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        _breaker_record_failure(url)
        return None


_UNSET = object()


class _DiskCache:
    """
    Tiny JSON-on-disk cache with a per-read TTL check.

    If no TTL is passed, CW_PRICE_TTL_SECONDS is read on every call so env
    changes take effect live. An explicit `ttl=` in the constructor wins.
    """

    def __init__(self, name: str, ttl=_UNSET):
        self.path = CACHE_DIR / f"{name}.json"
        self._explicit_ttl = ttl

    @property
    def ttl(self) -> int:
        if self._explicit_ttl is _UNSET:
            return _ttl_from_env()
        return self._explicit_ttl

    def read(self) -> tuple:
        """Returns (payload_or_None, fetched_at, is_fresh)."""
        if not self.path.exists():
            return (None, 0.0, False)
        try:
            body = json.loads(self.path.read_text())
        except (json.JSONDecodeError, OSError):
            return (None, 0.0, False)
        fetched_at = body.get("fetched_at", 0.0)
        age = time.time() - fetched_at
        return (body.get("data"), fetched_at, age < self.ttl)

    def write(self, data) -> None:
        try:
            from io_utils import write_json_atomic
            write_json_atomic(self.path, {"fetched_at": time.time(), "data": data}, indent=0)
        except OSError:
            pass


class PricingSource:
    name: str = "base"

    def get(self, model: str) -> Optional[SourcedPrice]:
        raise NotImplementedError

    def all_models(self) -> Dict[str, SourcedPrice]:
        """Optional: return every model this source knows about, keyed by slug."""
        return {}


# ---------------------------------------------------------------------------
# LiteLLM
# ---------------------------------------------------------------------------

class LiteLLMSource(PricingSource):
    """
    LiteLLM community pricing DB. Near-live, direct-from-provider prices.
    Schema per entry (subset):
      {
        "input_cost_per_token": 0.000003,
        "output_cost_per_token": 0.000015,
        "litellm_provider": "anthropic",
        "mode": "chat",
        ...
      }
    """
    name = "litellm"

    def __init__(self):
        self._cache = _DiskCache("litellm")

    def _data(self) -> tuple:
        """Returns (data, fetched_at). Network-first, stale-cache fallback."""
        payload, fetched_at, fresh = self._cache.read()
        if payload is not None and fresh:
            return payload, fetched_at
        fresh_data = _http_get_json(LITELLM_URL)
        if fresh_data is not None:
            self._cache.write(fresh_data)
            return fresh_data, time.time()
        # Network failed: return stale cache if we have it.
        return payload, fetched_at

    @staticmethod
    def _candidates(model: str) -> list:
        """Possible LiteLLM keys for a user-supplied model name."""
        cands = [model, model.lower()]
        if "/" in model:
            cands.append(model.split("/", 1)[1])
        return cands

    # Mode → (candidate cost fields, unit). Tried in order; first hit wins.
    _MODE_FIELDS = {
        "chat":                 [("input_cost_per_token", "output_cost_per_token", "token")],
        "completion":           [("input_cost_per_token", "output_cost_per_token", "token")],
        "responses":            [("input_cost_per_token", "output_cost_per_token", "token")],
        "embedding":            [("input_cost_per_token", "output_cost_per_token", "token")],
        "moderation":           [("input_cost_per_token", "output_cost_per_token", "token")],
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

    def _extract(self, entry: dict, mode: str) -> Optional[tuple]:
        """Return (input_per_1m, output_per_1m, unit) or None."""
        recipes = self._MODE_FIELDS.get(
            mode,
            [("input_cost_per_token", "output_cost_per_token", "token")],
        )
        for in_field, out_field, unit in recipes:
            inp_raw = entry.get(in_field) if in_field else None
            out_raw = entry.get(out_field) if out_field else None
            try:
                inp = float(inp_raw) if inp_raw is not None else 0.0
                outp = float(out_raw) if out_raw is not None else 0.0
            except (TypeError, ValueError):
                continue
            if inp == 0.0 and outp == 0.0:
                continue
            # Token / character costs are priced per-1; everything else is
            # already per-1. Scale uniformly to per-1M.
            return (inp * 1_000_000, outp * 1_000_000, unit)
        return None

    def get(self, model: str) -> Optional[SourcedPrice]:
        if _static_only():
            return None
        data, fetched_at = self._data()
        if not data:
            return None
        for key in self._candidates(model):
            entry = data.get(key)
            if not entry:
                continue
            mode = entry.get("mode") or "chat"
            result = self._extract(entry, mode)
            if result is None:
                continue
            inp, outp, unit = result
            return SourcedPrice(
                input_per_1m=inp,
                output_per_1m=outp,
                display_name=key,
                provider=entry.get("litellm_provider", "unknown"),
                source=self.name,
                fetched_at=fetched_at,
                mode=mode,
                unit=unit,
            )
        return None


# ---------------------------------------------------------------------------
# OpenRouter
# ---------------------------------------------------------------------------

class OpenRouterSource(PricingSource):
    """
    OpenRouter /api/v1/models — what you'd actually be billed if routing
    through OpenRouter. Schema per item (subset):
      {
        "id": "anthropic/claude-3-5-sonnet",
        "name": "...",
        "pricing": {"prompt": "0.000003", "completion": "0.000015"},
        ...
      }
    """
    name = "openrouter"

    def __init__(self):
        self._cache = _DiskCache("openrouter")

    def _data(self) -> tuple:
        payload, fetched_at, fresh = self._cache.read()
        if payload is not None and fresh:
            return payload, fetched_at
        fresh_data = _http_get_json(OPENROUTER_URL)
        if fresh_data is not None:
            self._cache.write(fresh_data)
            return fresh_data, time.time()
        return payload, fetched_at

    @staticmethod
    def _normalize(s: str) -> str:
        """Lowercase + dots→hyphens. Used for permissive cross-matching."""
        return s.lower().replace(".", "-")

    def _build_sourced_price(self, item: dict, fetched_at: float) -> Optional[SourcedPrice]:
        pricing = item.get("pricing") or {}
        try:
            inp = float(pricing.get("prompt", 0))
            outp = float(pricing.get("completion", 0))
        except (TypeError, ValueError):
            return None
        return SourcedPrice(
            input_per_1m=inp * 1_000_000,
            output_per_1m=outp * 1_000_000,
            display_name=item.get("name") or item.get("id", ""),
            provider="openrouter",
            source=self.name,
            fetched_at=fetched_at,
            mode="chat",
            unit="token",
        )

    def get(self, model: str) -> Optional[SourcedPrice]:
        """
        Strict match: only returns a result when the query has `openrouter/`
        prefix AND OpenRouter has that exact ID. For fuzzy fallback use
        `get_permissive`.
        """
        if _static_only():
            return None
        data, fetched_at = self._data()
        if not data:
            return None
        if not model.startswith("openrouter/"):
            return None
        query = model[len("openrouter/"):]
        for item in data.get("data", []):
            if item.get("id") == query:
                return self._build_sourced_price(item, fetched_at)
        return None

    def get_permissive(self, model: str) -> Optional[SourcedPrice]:
        """
        Fuzzy fallback. Matches any OpenRouter ID whose suffix equals the
        normalized query (lowercase, dots→hyphens). Used by the router
        when LiteLLM misses on a non-prefixed query.
        """
        if _static_only():
            return None
        data, fetched_at = self._data()
        if not data:
            return None
        q = self._normalize(model.split("openrouter/", 1)[-1])
        for item in data.get("data", []):
            mid = item.get("id", "")
            if not mid:
                continue
            norm = self._normalize(mid)
            # Suffix match: "claude-sonnet-4-6" matches "anthropic/claude-sonnet-4-6"
            # but not the other way — that way "gpt-4o" doesn't spuriously match
            # some unrelated "gpt-4o-long-name".
            if norm == q or norm.endswith("/" + q):
                return self._build_sourced_price(item, fetched_at)
        return None


# ---------------------------------------------------------------------------
# Static markdown (offline fallback)
# ---------------------------------------------------------------------------

class StaticMarkdownSource(PricingSource):
    """Parses references/pricing.md. Always-available fallback."""
    name = "static"

    def __init__(self):
        self._cached: Dict[str, SourcedPrice] = {}
        self._cached_mtime: float = -1.0

    def _parse_cell(self, cell: str) -> Optional[float]:
        cell = cell.strip()
        if not cell or cell in ("—", "-"):
            return None
        m = _PRICE_RE.search(cell)
        return float(m.group(1)) if m else None

    def _parse_section_header(self, header: str) -> tuple:
        """
        Extract (provider, mode, unit) from a section heading like:
          "## OpenAI — image_generation (per image)"
          "## Anthropic — chat (per 1M tokens)"
          "## Anthropic"   (legacy; defaults to mode=chat, unit=token)
        Returns (provider, mode, unit).
        """
        body = header.strip()[3:].strip()
        mode, unit = "chat", "token"

        # Pull "(per ...)" qualifier if present.
        qual_match = re.search(r"\(per\s+(?:[\d,]+M\s+)?([a-z]+)\)", body, re.IGNORECASE)
        if qual_match:
            raw = qual_match.group(1).lower()
            # Accept both singular and plural (tokens, queries, pages, ...).
            plural_to_singular = {
                "tokens": "token", "images": "image", "seconds": "second",
                "queries": "query", "pages": "page", "characters": "character",
                "pixels": "pixel",
            }
            raw_unit = plural_to_singular.get(raw, raw)
            if raw_unit in ("token", "image", "second", "query", "page",
                            "character", "pixel"):
                unit = raw_unit
            body = body[:qual_match.start()].strip()

        # Pull "— <mode>" qualifier if present.
        for sep in ("—", "--", " - "):
            if sep in body:
                provider_part, mode_part = body.split(sep, 1)
                provider = provider_part.strip()
                mode = mode_part.strip()
                return provider, mode, unit

        return body, mode, unit

    def _ensure_loaded(self) -> None:
        if not _PRICING_MD.exists():
            self._cached = {}
            return
        mtime = _PRICING_MD.stat().st_mtime
        if mtime == self._cached_mtime and self._cached:
            return

        out: Dict[str, SourcedPrice] = {}
        provider, mode, unit = "unknown", "chat", "token"
        for raw in _PRICING_MD.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line.startswith("## "):
                provider, mode, unit = self._parse_section_header(line)
                continue
            if "|" not in line or "$" not in line:
                continue
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) < 3:
                continue
            name = parts[0]
            if not name or not re.match(r"^[A-Za-z0-9]", name):
                continue
            if name.lower() == "model":
                continue
            inp = self._parse_cell(parts[1])
            outp = self._parse_cell(parts[2])
            if inp is None or outp is None:
                continue
            slug = canonical_slug(name)
            if slug in out:
                continue
            out[slug] = SourcedPrice(
                input_per_1m=inp,
                output_per_1m=outp,
                display_name=name,
                provider=provider,
                source=self.name,
                fetched_at=0.0,
                mode=mode,
                unit=unit,
            )
        self._cached = out
        self._cached_mtime = mtime

    def get(self, model: str) -> Optional[SourcedPrice]:
        self._ensure_loaded()
        return self._cached.get(canonical_slug(model))

    def all_models(self) -> Dict[str, SourcedPrice]:
        self._ensure_loaded()
        return dict(self._cached)
