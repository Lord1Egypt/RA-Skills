"""
SDK wrappers that record every LLM call to usage.jsonl.

Usage:
    # OpenAI / any OpenAI-compatible provider (OpenRouter, Groq, DeepSeek, ...)
    from tracker import track_openai
    import openai
    client = track_openai(openai.OpenAI())

    # Anthropic direct
    from tracker import track_anthropic
    import anthropic
    client = track_anthropic(anthropic.Anthropic())

Both wrappers:
  - Intercept chat.completions.create / messages.create (sync + async).
  - Read model + usage from the response object.
  - Price via _pricing.get_price (live LiteLLM/OpenRouter with static fallback).
  - Append one row per call to ~/.cost-watchdog/usage.jsonl.
  - Optional: raise BudgetExceeded if a budget ceiling is set and crossed.

No vendored dependencies — we import the SDKs lazily so tracker.py is
importable even if openai/anthropic aren't installed.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any, Callable, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
import usage_log  # noqa: E402
import _pricing   # noqa: E402
import errors     # noqa: E402


def _report_error(component: str, exc: BaseException) -> None:
    """Log a swallowed exception without ever raising."""
    try:
        errors.log_error(component, exc)
    except Exception:
        pass


class BudgetExceeded(RuntimeError):
    """Raised when a call would push cumulative spend past the ceiling."""


# ---------------------------------------------------------------------------
# Streaming wrappers — OpenAI + Anthropic streams emit usage in the final chunk.
# ---------------------------------------------------------------------------

class _TrackedOpenAIStream:
    """
    Wraps an openai stream so iterating it captures the final chunk's usage.
    Relies on stream_options={'include_usage': True} being set — we inject
    that automatically in the wrapper.
    """
    def __init__(self, stream, log_fn, enforce):
        self._stream = stream
        self._log_fn = log_fn
        self._enforce = enforce
        self._last_with_usage = None
        self._logged = False

    def __iter__(self):
        for chunk in self._stream:
            if getattr(chunk, "usage", None) is not None:
                self._last_with_usage = chunk
            yield chunk
        self._finalize()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._finalize()
        try:
            return self._stream.__exit__(*exc)
        except AttributeError:
            return False

    def __getattr__(self, name):
        return getattr(self._stream, name)

    def _finalize(self):
        if self._logged or self._last_with_usage is None:
            return
        self._logged = True
        entry = self._log_fn(self._last_with_usage)
        try:
            self._enforce(entry.get("cost_total", 0.0), entry.get("session_id"))
        except BudgetExceeded:
            raise


class _TrackedAnthropicStream:
    """
    Wraps Anthropic's MessageStreamManager (returned by stream=True).
    We hook the manager's __exit__ to fetch the final message's usage.
    """
    def __init__(self, manager, log_fn, enforce):
        self._manager = manager
        self._log_fn = log_fn
        self._enforce = enforce

    def __enter__(self):
        self._entered = self._manager.__enter__()
        return self._entered

    def __exit__(self, *exc):
        try:
            stream = self._entered
            final = getattr(stream, "get_final_message", lambda: None)()
            if final is not None:
                entry = self._log_fn(final)
                try:
                    self._enforce(entry.get("cost_total", 0.0), entry.get("session_id"))
                except BudgetExceeded:
                    raise
        finally:
            return self._manager.__exit__(*exc)


# ---------------------------------------------------------------------------
# Budget check
# ---------------------------------------------------------------------------

def _budget_from_env() -> Optional[float]:
    """CW_BUDGET_USD sets a session-or-lifetime ceiling. Unset = no check."""
    raw = os.environ.get("CW_BUDGET_USD")
    if raw is None:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def _enforce_budget(next_cost: float, session_id: Optional[str]) -> None:
    """
    Post-append budget check. The real race-safe enforcement lives inside
    append_usage() — this function is used by wrappers that have already
    logged and just want a hard stop if we're now over.

    The logged cost is already in the total, so we compare directly.
    """
    ceiling = _budget_from_env()
    if ceiling is None:
        return
    current = usage_log.session_total(session_id=session_id).get("cost_total", 0.0)
    if current > ceiling:
        raise BudgetExceeded(
            f"Budget ${ceiling:.2f} exceeded: cumulative ${current:.4f}."
        )


# ---------------------------------------------------------------------------
# Helpers — pricing + usage extraction
# ---------------------------------------------------------------------------

def _price_call(model: Optional[str],
                input_tokens: int, output_tokens: int) -> tuple:
    """Return (cost_input, cost_output, cost_total, unit)."""
    if not model:
        return (0.0, 0.0, 0.0, "unknown")
    price = _pricing.get_price(model)
    if price is None or price.unit != "token":
        return (0.0, 0.0, 0.0, price.unit if price else "unknown")
    cost_in = (input_tokens / 1_000_000) * price.input_per_1m
    cost_out = (output_tokens / 1_000_000) * price.output_per_1m
    return (cost_in, cost_out, cost_in + cost_out, "token")


def _getattr_path(obj: Any, *names: str, default=None) -> Any:
    """Safely walk nested attrs: _getattr_path(resp, 'usage', 'input_tokens')."""
    cur = obj
    for n in names:
        if cur is None:
            return default
        cur = getattr(cur, n, None)
    return cur if cur is not None else default


def _as_int(v) -> int:
    try:
        return int(v or 0)
    except (TypeError, ValueError):
        return 0


# ---------------------------------------------------------------------------
# OpenAI wrapper
# ---------------------------------------------------------------------------

def _log_openai_response(response: Any, source: str,
                         session_id: Optional[str]) -> dict:
    """Extract usage + cost from an OpenAI-shape response. Returns the logged row."""
    model = _getattr_path(response, "model") or "unknown"
    usage = _getattr_path(response, "usage")

    # OpenAI: prompt_tokens / completion_tokens / prompt_tokens_details.cached_tokens
    input_tokens = _as_int(_getattr_path(usage, "prompt_tokens"))
    output_tokens = _as_int(_getattr_path(usage, "completion_tokens"))
    cache_read = _as_int(_getattr_path(usage, "prompt_tokens_details", "cached_tokens"))

    cost_in, cost_out, cost_total, unit = _price_call(model, input_tokens, output_tokens)

    entry = {
        "source": source,
        "model": model,
        "provider": _guess_openai_provider(response),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_tokens": cache_read,
        "cache_write_tokens": 0,
        "cost_input": cost_in,
        "cost_output": cost_out,
        "cost_total": cost_total,
        "session_id": session_id,
        "extra": {"pricing_unit": unit},
    }
    usage_log.append_usage(entry)
    return entry


def _guess_openai_provider(response: Any) -> str:
    """Guess the provider from response metadata. Heuristic."""
    sys_fp = _getattr_path(response, "system_fingerprint") or ""
    model = (_getattr_path(response, "model") or "").lower()
    if "anthropic" in model or "claude" in model:
        return "anthropic"
    if "gemini" in model or "google" in model:
        return "google"
    if "llama" in model or "mistral" in model or "deepseek" in model:
        return model.split("/")[0] if "/" in model else "openai-compatible"
    return "openai"


def track_openai(client: Any, *, source: str = "openai-wrap",
                 session_id: Optional[str] = None) -> Any:
    """
    Wrap an openai.OpenAI (or AsyncOpenAI) client so every
    chat.completions.create call — sync, async, or streaming — is logged.
    """
    log_fn = lambda resp: _log_openai_response(resp, source=source, session_id=session_id)
    _patch_openai_create(client, ("chat", "completions"), log_fn, session_id)
    try:
        _patch_openai_create(client, ("responses",), log_fn, session_id)
    except AttributeError:
        pass
    return client


def _patch_openai_create(client, path, log_fn, session_id):
    """
    OpenAI create() returns either a response object or a stream. If the
    caller set stream=True we inject stream_options={'include_usage': True}
    and return a tee'd stream wrapper that logs the last chunk's usage.
    """
    ns = client
    for attr in path:
        ns = getattr(ns, attr)
    original = ns.create

    def enforce(cost, sid):
        _enforce_budget(cost, sid)

    def wrapper(*args, **kwargs):
        is_stream = bool(kwargs.get("stream"))
        if is_stream:
            so = dict(kwargs.get("stream_options") or {})
            so.setdefault("include_usage", True)
            kwargs["stream_options"] = so
        result = original(*args, **kwargs)
        if is_stream:
            return _TrackedOpenAIStream(result, log_fn, enforce)
        try:
            entry = log_fn(result)
            enforce(entry.get("cost_total", 0.0), entry.get("session_id"))
        except BudgetExceeded:
            raise
        except Exception as e:
            _report_error("openai-wrap", e)
        return result

    ns.create = wrapper


# ---------------------------------------------------------------------------
# Anthropic wrapper
# ---------------------------------------------------------------------------

def _log_anthropic_response(response: Any, source: str,
                            session_id: Optional[str]) -> dict:
    model = _getattr_path(response, "model") or "unknown"
    usage = _getattr_path(response, "usage")

    # Anthropic: input_tokens / output_tokens / cache_read_input_tokens / cache_creation_input_tokens
    input_tokens = _as_int(_getattr_path(usage, "input_tokens"))
    output_tokens = _as_int(_getattr_path(usage, "output_tokens"))
    cache_read = _as_int(_getattr_path(usage, "cache_read_input_tokens"))
    cache_write = _as_int(_getattr_path(usage, "cache_creation_input_tokens"))

    cost_in, cost_out, cost_total, unit = _price_call(model, input_tokens, output_tokens)

    entry = {
        "source": source,
        "model": model,
        "provider": "anthropic",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_tokens": cache_read,
        "cache_write_tokens": cache_write,
        "cost_input": cost_in,
        "cost_output": cost_out,
        "cost_total": cost_total,
        "session_id": session_id,
        "extra": {
            "pricing_unit": unit,
            "stop_reason": _getattr_path(response, "stop_reason"),
        },
    }
    usage_log.append_usage(entry)
    return entry


def track_anthropic(client: Any, *, source: str = "anthropic-wrap",
                    session_id: Optional[str] = None) -> Any:
    """Wrap anthropic.Anthropic / AsyncAnthropic, including .messages.stream."""
    log_fn = lambda resp: _log_anthropic_response(resp, source=source, session_id=session_id)

    # Non-streaming .messages.create()
    _patch_namespaced_method(client, ("messages",), "create", log_fn)

    # Streaming .messages.stream() — returns a MessageStreamManager
    try:
        messages_ns = client.messages
        original_stream = messages_ns.stream

        def stream_wrapper(*args, **kwargs):
            manager = original_stream(*args, **kwargs)
            return _TrackedAnthropicStream(
                manager, log_fn,
                lambda cost, sid: _enforce_budget(cost, sid),
            )
        messages_ns.stream = stream_wrapper
    except AttributeError:
        pass

    return client


# ---------------------------------------------------------------------------
# Gemini wrapper (google-generativeai)
# ---------------------------------------------------------------------------

def _log_gemini_response(response: Any, model_hint: Optional[str],
                        source: str, session_id: Optional[str]) -> dict:
    # Gemini: response.usage_metadata has prompt_token_count,
    # candidates_token_count, and total_token_count.
    model = model_hint or "gemini-unknown"
    usage = _getattr_path(response, "usage_metadata")
    input_tokens = _as_int(_getattr_path(usage, "prompt_token_count"))
    output_tokens = _as_int(_getattr_path(usage, "candidates_token_count"))
    cached_tokens = _as_int(_getattr_path(usage, "cached_content_token_count"))
    cost_in, cost_out, cost_total, unit = _price_call(model, input_tokens, output_tokens)
    entry = {
        "source": source,
        "model": model,
        "provider": "google",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_tokens": cached_tokens,
        "cache_write_tokens": 0,
        "cost_input": cost_in,
        "cost_output": cost_out,
        "cost_total": cost_total,
        "session_id": session_id,
        "extra": {"pricing_unit": unit},
    }
    usage_log.append_usage(entry)
    return entry


def track_gemini(model_instance: Any, *, source: str = "gemini-wrap",
                 session_id: Optional[str] = None) -> Any:
    """
    Wrap a google.generativeai.GenerativeModel so generate_content is logged.
    Usage: model = track_gemini(genai.GenerativeModel('gemini-2.0-flash'))
    """
    model_name = _getattr_path(model_instance, "model_name") or "gemini-unknown"
    # model_name often comes as "models/gemini-2.0-flash" — strip prefix.
    if isinstance(model_name, str) and model_name.startswith("models/"):
        model_name = model_name[len("models/"):]

    _patch_instance_method(
        model_instance, "generate_content",
        lambda resp: _log_gemini_response(resp, model_name, source, session_id),
    )
    return model_instance


# ---------------------------------------------------------------------------
# Cohere wrapper
# ---------------------------------------------------------------------------

def _log_cohere_response(response: Any, source: str,
                        session_id: Optional[str]) -> dict:
    # Cohere v2: response.usage.billed_units has input_tokens / output_tokens
    # (v1 uses response.meta.tokens). Try both.
    usage = (_getattr_path(response, "usage", "billed_units")
             or _getattr_path(response, "meta", "tokens"))
    input_tokens = _as_int(
        _getattr_path(usage, "input_tokens")
        or _getattr_path(usage, "input")
    )
    output_tokens = _as_int(
        _getattr_path(usage, "output_tokens")
        or _getattr_path(usage, "output")
    )
    model = _getattr_path(response, "model") or "cohere-unknown"
    cost_in, cost_out, cost_total, unit = _price_call(model, input_tokens, output_tokens)
    entry = {
        "source": source,
        "model": model,
        "provider": "cohere",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_tokens": 0,
        "cache_write_tokens": 0,
        "cost_input": cost_in,
        "cost_output": cost_out,
        "cost_total": cost_total,
        "session_id": session_id,
        "extra": {"pricing_unit": unit},
    }
    usage_log.append_usage(entry)
    return entry


def track_cohere(client: Any, *, source: str = "cohere-wrap",
                 session_id: Optional[str] = None) -> Any:
    """Wrap a cohere.ClientV2 / cohere.Client so .chat is logged."""
    _patch_instance_method(
        client, "chat",
        lambda resp: _log_cohere_response(resp, source, session_id),
    )
    return client


# ---------------------------------------------------------------------------
# Bedrock wrapper (boto3)
# ---------------------------------------------------------------------------

def _log_bedrock_response(response: dict, model_hint: str, source: str,
                         session_id: Optional[str]) -> dict:
    # boto3's bedrock-runtime.invoke_model returns a dict with a StreamingBody
    # we can't re-read here without disrupting user code. Rely on
    # response['ResponseMetadata']['HTTPHeaders'] — Bedrock returns
    # x-amzn-bedrock-input-token-count and x-amzn-bedrock-output-token-count.
    headers = (response.get("ResponseMetadata") or {}).get("HTTPHeaders") or {}
    input_tokens = _as_int(headers.get("x-amzn-bedrock-input-token-count"))
    output_tokens = _as_int(headers.get("x-amzn-bedrock-output-token-count"))
    model = model_hint or "bedrock-unknown"
    cost_in, cost_out, cost_total, unit = _price_call(model, input_tokens, output_tokens)
    entry = {
        "source": source,
        "model": model,
        "provider": "bedrock",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_tokens": 0,
        "cache_write_tokens": 0,
        "cost_input": cost_in,
        "cost_output": cost_out,
        "cost_total": cost_total,
        "session_id": session_id,
        "extra": {"pricing_unit": unit},
    }
    usage_log.append_usage(entry)
    return entry


def track_bedrock(client: Any, *, source: str = "bedrock-wrap",
                  session_id: Optional[str] = None) -> Any:
    """
    Wrap a boto3 bedrock-runtime client so invoke_model / converse are logged.
    Usage: client = track_bedrock(boto3.client('bedrock-runtime'))
    """
    original = getattr(client, "invoke_model", None)
    if original is None:
        return client  # not a bedrock-runtime client

    def wrapper(*args, **kwargs):
        model_hint = kwargs.get("modelId", "bedrock-unknown")
        resp = original(*args, **kwargs)
        try:
            entry = _log_bedrock_response(resp, model_hint, source, session_id)
            _enforce_budget(entry.get("cost_total", 0.0), entry.get("session_id"))
        except BudgetExceeded:
            raise
        except Exception as _exc:
            _report_error("tracker", _exc)
        return resp
    client.invoke_model = wrapper

    converse = getattr(client, "converse", None)
    if converse is not None:
        def converse_wrapper(*args, **kwargs):
            model_hint = kwargs.get("modelId", "bedrock-unknown")
            resp = converse(*args, **kwargs)
            try:
                usage = resp.get("usage") or {}
                input_tokens = int(usage.get("inputTokens", 0))
                output_tokens = int(usage.get("outputTokens", 0))
                cost_in, cost_out, cost_total, unit = _price_call(
                    model_hint, input_tokens, output_tokens
                )
                usage_log.append_usage({
                    "source": source,
                    "model": model_hint,
                    "provider": "bedrock",
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "cache_read_tokens": 0,
                    "cache_write_tokens": 0,
                    "cost_input": cost_in,
                    "cost_output": cost_out,
                    "cost_total": cost_total,
                    "session_id": session_id,
                    "extra": {"pricing_unit": unit, "api": "converse"},
                })
                _enforce_budget(cost_total, session_id)
            except BudgetExceeded:
                raise
            except Exception as _exc:
                _report_error("tracker", _exc)
            return resp
        client.converse = converse_wrapper

    return client


# ---------------------------------------------------------------------------
# Patching primitive — wraps an instance method, preserves type
# ---------------------------------------------------------------------------

def _patch_instance_method(obj: Any, method_name: str,
                           after_call: Callable[[Any], dict]) -> None:
    """Wrap obj.<method_name> so after_call runs on every return value."""
    import inspect
    original = getattr(obj, method_name)
    if inspect.iscoroutinefunction(original):
        async def wrapper(*args, **kwargs):
            resp = await original(*args, **kwargs)
            try:
                entry = after_call(resp)
                _enforce_budget(entry.get("cost_total", 0.0), entry.get("session_id"))
            except BudgetExceeded:
                raise
            except Exception as _exc:
                _report_error("tracker", _exc)
            return resp
    else:
        def wrapper(*args, **kwargs):
            resp = original(*args, **kwargs)
            try:
                entry = after_call(resp)
                _enforce_budget(entry.get("cost_total", 0.0), entry.get("session_id"))
            except BudgetExceeded:
                raise
            except Exception as _exc:
                _report_error("tracker", _exc)
            return resp
    setattr(obj, method_name, wrapper)


def _patch_namespaced_method(client: Any, path: tuple, method_name: str,
                             after_call: Callable[[Any], dict]) -> None:
    """
    Patch `client.<path[0]>.<path[1]>.<method_name>` to call the original,
    then run `after_call(result)`. Also handles async versions via `inspect.iscoroutinefunction`.
    """
    import inspect

    ns = client
    for attr in path:
        ns = getattr(ns, attr)
    original = getattr(ns, method_name)

    if inspect.iscoroutinefunction(original):
        async def wrapper(*args, **kwargs):
            resp = await original(*args, **kwargs)
            try:
                entry = after_call(resp)
                _enforce_budget(entry.get("cost_total", 0.0), entry.get("session_id"))
            except BudgetExceeded:
                raise
            except Exception as _exc:
                _report_error("tracker", _exc)
            return resp
    else:
        def wrapper(*args, **kwargs):
            resp = original(*args, **kwargs)
            try:
                entry = after_call(resp)
                _enforce_budget(entry.get("cost_total", 0.0), entry.get("session_id"))
            except BudgetExceeded:
                raise
            except Exception as _exc:
                _report_error("tracker", _exc)
            return resp

    setattr(ns, method_name, wrapper)


# ---------------------------------------------------------------------------
# Tiny stub fixtures for tests — let us exercise the wrappers without real SDKs
# ---------------------------------------------------------------------------

class _StubNamespace:
    """Minimal attribute bag used to simulate client.chat.completions.create etc."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def _make_fake_openai_client(response):
    """Return an object shaped like openai.OpenAI with a chat.completions.create."""
    def create(**_kwargs):
        return response
    ns = _StubNamespace(chat=_StubNamespace(completions=_StubNamespace(create=create)))
    return ns


def _make_fake_anthropic_client(response):
    def create(**_kwargs):
        return response
    return _StubNamespace(messages=_StubNamespace(create=create))
