"""
HTTP-layer capture: log LLM calls without wrapping any SDK.

The modern Python SDKs (openai, anthropic, google-genai, cohere, mistralai)
all use `httpx` under the hood. Monkey-patching httpx's transport lets us
observe every LLM HTTP request and response from those SDKs — no user code
changes needed.

Usage:
    from http_capture import install_global_capture
    install_global_capture()   # call once at process start

Not captured:
    - SDKs that use `requests`/`urllib3` directly (older Cohere, boto3).
      Use the per-SDK wrappers in tracker.py for those.
    - Streaming responses (we read usage from the final body, which means
      the stream has to have finished).

This is best-effort telemetry. For strict billing you still want the
provider's own dashboard.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import usage_log  # noqa: E402
import _pricing   # noqa: E402


# (host_suffix, provider_tag)
_KNOWN_HOSTS = [
    ("api.anthropic.com", "anthropic"),
    ("api.openai.com", "openai"),
    ("openrouter.ai", "openrouter"),
    ("api.mistral.ai", "mistral"),
    ("api.cohere.com", "cohere"),
    ("api.cohere.ai", "cohere"),
    ("api.deepseek.com", "deepseek"),
    ("api.groq.com", "groq"),
    ("generativelanguage.googleapis.com", "google"),
    ("api.x.ai", "xai"),
    ("api.together.xyz", "together"),
    ("api.fireworks.ai", "fireworks"),
    ("api.perplexity.ai", "perplexity"),
]


def _classify_host(host: str) -> Optional[str]:
    host = host.lower()
    for suffix, tag in _KNOWN_HOSTS:
        if host.endswith(suffix):
            return tag
    return None


def _extract_model_and_usage(provider: str, body: dict) -> Tuple[Optional[str], int, int, int, int]:
    """
    Return (model, input_tokens, output_tokens, cache_read, cache_write).
    Handles OpenAI-style, Anthropic-style, and Gemini-style bodies.
    Zeros for anything missing.
    """
    if not isinstance(body, dict):
        return (None, 0, 0, 0, 0)

    model = body.get("model") or body.get("modelId")

    # OpenAI-style: body["usage"] = {prompt_tokens, completion_tokens, ...}
    u = body.get("usage") or {}
    if "prompt_tokens" in u or "completion_tokens" in u:
        input_t = int(u.get("prompt_tokens", 0))
        output_t = int(u.get("completion_tokens", 0))
        cache_r = int((u.get("prompt_tokens_details") or {}).get("cached_tokens", 0))
        return (model, input_t, output_t, cache_r, 0)

    # Anthropic-style: usage = {input_tokens, output_tokens, ...}
    if "input_tokens" in u or "output_tokens" in u:
        input_t = int(u.get("input_tokens", 0))
        output_t = int(u.get("output_tokens", 0))
        cache_r = int(u.get("cache_read_input_tokens", 0))
        cache_w = int(u.get("cache_creation_input_tokens", 0))
        return (model, input_t, output_t, cache_r, cache_w)

    # Gemini-style: body["usageMetadata"]
    um = body.get("usageMetadata") or body.get("usage_metadata") or {}
    if um:
        input_t = int(um.get("promptTokenCount", um.get("prompt_token_count", 0)))
        output_t = int(um.get("candidatesTokenCount", um.get("candidates_token_count", 0)))
        cache_r = int(um.get("cachedContentTokenCount", um.get("cached_content_token_count", 0)))
        return (model, input_t, output_t, cache_r, 0)

    # Cohere v2: body["meta"]["billed_units"] or body["meta"]["tokens"]
    meta = body.get("meta") or {}
    units = meta.get("billed_units") or meta.get("tokens") or {}
    if units:
        input_t = int(units.get("input_tokens", units.get("input", 0)))
        output_t = int(units.get("output_tokens", units.get("output", 0)))
        return (model, input_t, output_t, 0, 0)

    return (model, 0, 0, 0, 0)


def _log_http_call(provider: str, body: dict) -> None:
    model, inp, out, cr, cw = _extract_model_and_usage(provider, body)
    if not model or (inp == 0 and out == 0):
        # Not a priceable LLM call (could be a list_models, health check, etc.)
        return
    price = _pricing.get_price(model)
    if price and price.unit == "token":
        cost_in = (inp / 1_000_000) * price.input_per_1m
        cost_out = (out / 1_000_000) * price.output_per_1m
        cost_total = cost_in + cost_out
    else:
        cost_in = cost_out = cost_total = 0.0
    usage_log.append_usage({
        "source": f"http-capture/{provider}",
        "model": model,
        "provider": provider,
        "input_tokens": inp,
        "output_tokens": out,
        "cache_read_tokens": cr,
        "cache_write_tokens": cw,
        "cost_input": cost_in,
        "cost_output": cost_out,
        "cost_total": cost_total,
        "session_id": None,
        "extra": {"via": "httpx_transport"},
    })


_INSTALLED = False


def install_global_capture() -> bool:
    """
    Monkey-patch httpx.HTTPTransport.handle_request so every request to a
    known LLM host gets logged. Returns True if installed, False if httpx
    isn't available.
    """
    global _INSTALLED
    if _INSTALLED:
        return True
    try:
        import httpx
    except ImportError:
        return False

    original_sync = httpx.HTTPTransport.handle_request

    def sync_wrapped(self, request):
        response = original_sync(self, request)
        try:
            _maybe_log(request, response)
        except Exception:
            pass
        return response

    httpx.HTTPTransport.handle_request = sync_wrapped

    # Async transport (AsyncHTTPTransport) — patch the async path too.
    if hasattr(httpx, "AsyncHTTPTransport"):
        original_async = httpx.AsyncHTTPTransport.handle_async_request

        async def async_wrapped(self, request):
            response = await original_async(self, request)
            try:
                _maybe_log(request, response)
            except Exception:
                pass
            return response

        httpx.AsyncHTTPTransport.handle_async_request = async_wrapped

    _INSTALLED = True
    return True


def _maybe_log(request, response) -> None:
    """Inspect a finished httpx request/response pair and log if it's an LLM call."""
    host = urlsplit(str(request.url)).netloc
    provider = _classify_host(host)
    if provider is None:
        return

    content_type = (response.headers.get("content-type") or "").lower()

    # Streaming (SSE / chunked). We can't read the final usage chunk here —
    # the user owns the stream. Record the gap so it's visible.
    if "text/event-stream" in content_type:
        _report_stream_gap(provider, str(request.url))
        return

    if "application/json" not in content_type:
        return

    # httpx response.content is only populated for non-streaming responses.
    # For streams the user read with iter_lines(), .content raises.
    try:
        raw = response.content
    except Exception:
        _report_stream_gap(provider, str(request.url))
        return
    try:
        body = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError, AttributeError):
        return
    _log_http_call(provider, body)


def _report_stream_gap(provider: str, url: str) -> None:
    """Emit a single errors.jsonl entry noting a streaming call we couldn't price."""
    try:
        from errors import log_error
        log_error("http_capture", f"skipped stream: provider={provider} url={url}",
                  hint="Use track_openai / track_anthropic for streaming coverage.")
    except Exception:
        pass


if __name__ == "__main__":
    installed = install_global_capture()
    print("http capture installed." if installed else "httpx not available.")
