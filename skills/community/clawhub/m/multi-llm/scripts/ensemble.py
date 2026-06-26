#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "anthropic>=0.40.0",
#     "openai>=1.0.0",
#     "google-genai>=1.0.0",
#     "httpx>=0.27.0",
# ]
# ///
"""
Mixture of Agents (MoA) ensemble script.
Queries multiple LLM providers in parallel, then synthesizes the best answer.
"""

import argparse
import asyncio
import json
import os
import pathlib
import sys
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MODEL_TIMEOUT = 90          # seconds per proposer model call
SYNTH_TIMEOUT = 120         # seconds for synthesis call
MAX_RESPONSE_CHARS = 6_000  # truncate proposer responses before synthesis
MAX_ROUNDS = 5

PROVIDER_PRIORITY = ["anthropic", "openai", "gemini", "ollama"]

DEFAULT_MODELS: dict[str, list[str]] = {
    "anthropic": ["claude-sonnet-4-6", "claude-haiku-4-5-20251001"],
    "openai": ["gpt-4o", "gpt-4o-mini"],
    "gemini": ["gemini-2.0-flash", "gemini-1.5-pro"],
}

SYNTHESIZER_PRIORITY = [
    ("anthropic", "claude-opus-4-7"),
    ("anthropic", "claude-sonnet-4-6"),
    ("openai", "gpt-4o"),
    ("gemini", "gemini-1.5-pro"),
]

# Sensitive path prefixes that --output should never touch
_SENSITIVE_PREFIXES = (
    "/etc/", "/sys/", "/proc/", "/boot/",
    "C:\\Windows\\", "C:\\System32\\",
)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ModelResponse:
    model: str
    provider: str
    content: str
    error: Optional[str] = None


@dataclass
class EnsembleResult:
    synthesis: str
    proposer_responses: list[ModelResponse] = field(default_factory=list)
    synthesizer_model: str = ""
    rounds: int = 1


# ---------------------------------------------------------------------------
# Lazy-cached client singletons (created once, reused across parallel calls)
# ---------------------------------------------------------------------------

_clients: dict = {}


def _get_anthropic():
    if "anthropic" not in _clients:
        import anthropic
        _clients["anthropic"] = anthropic.AsyncAnthropic()
    return _clients["anthropic"]


def _get_openai():
    if "openai" not in _clients:
        from openai import AsyncOpenAI
        _clients["openai"] = AsyncOpenAI()
    return _clients["openai"]


def _get_gemini():
    if "gemini" not in _clients:
        from google import genai
        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY not set")
        _clients["gemini"] = genai.Client(api_key=key)
    return _clients["gemini"]


def _get_httpx():
    if "httpx" not in _clients:
        import httpx
        _clients["httpx"] = httpx.AsyncClient(timeout=MODEL_TIMEOUT)
    return _clients["httpx"]


async def _close_clients() -> None:
    if "httpx" in _clients:
        await _clients["httpx"].aclose()


# ---------------------------------------------------------------------------
# Security validation helpers
# ---------------------------------------------------------------------------

def validate_ollama_host(host: str) -> str:
    parsed = urlparse(host)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            f"OLLAMA_HOST must use http:// or https://, got: {host!r}"
        )
    if not parsed.netloc:
        raise ValueError(f"OLLAMA_HOST has no hostname: {host!r}")
    return host.rstrip("/")


def validate_output_path(path: str) -> pathlib.Path:
    resolved = pathlib.Path(path).resolve()
    resolved_str = str(resolved)
    for prefix in _SENSITIVE_PREFIXES:
        if resolved_str.lower().startswith(prefix.lower()):
            raise ValueError(
                f"Refusing to write to sensitive path: {resolved_str}"
            )
    return resolved


# ---------------------------------------------------------------------------
# Provider detection
# ---------------------------------------------------------------------------

def detect_providers() -> dict[str, bool]:
    ollama_host = os.environ.get("OLLAMA_HOST", "")
    ollama_ok = False
    if ollama_host:
        try:
            validate_ollama_host(ollama_host)
            ollama_ok = True
        except ValueError as e:
            print(f"[warn] OLLAMA_HOST invalid, skipping: {e}", file=sys.stderr)
    else:
        # Default localhost is always attempted if no explicit host is set
        ollama_ok = True

    return {
        "anthropic": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "openai": bool(os.environ.get("OPENAI_API_KEY")),
        "gemini": bool(os.environ.get("GEMINI_API_KEY")),
        "ollama": ollama_ok,
    }


async def list_ollama_models(host: str) -> list[str]:
    try:
        client = _get_httpx()
        r = await asyncio.wait_for(
            client.get(f"{host}/api/tags"), timeout=5
        )
        r.raise_for_status()
        return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        return []


async def build_model_list(
    requested: Optional[list[str]], providers: dict[str, bool]
) -> list[tuple[str, str]]:
    if requested:
        result = []
        for model in requested:
            provider = infer_provider(model)
            if provider and providers.get(provider):
                result.append((provider, model))
            elif provider and not providers.get(provider):
                print(
                    f"[warn] Provider for '{model}' not available (missing API key?)",
                    file=sys.stderr,
                )
            else:
                print(
                    f"[warn] Cannot infer provider for '{model}', skipping",
                    file=sys.stderr,
                )
        return result

    result = []
    for provider in PROVIDER_PRIORITY:
        if not providers.get(provider):
            continue
        if provider == "ollama":
            host = validate_ollama_host(
                os.environ.get("OLLAMA_HOST", "http://localhost:11434")
            )
            ollama_models = await list_ollama_models(host)
            for m in ollama_models[:2]:
                result.append(("ollama", m))
        else:
            for m in DEFAULT_MODELS.get(provider, []):
                result.append((provider, m))
    return result


def infer_provider(model: str) -> Optional[str]:
    m = model.lower()
    if "claude" in m:
        return "anthropic"
    if "gpt" in m or m.startswith("o1") or m.startswith("o3"):
        return "openai"
    if "gemini" in m:
        return "gemini"
    return None


def pick_synthesizer(
    requested: Optional[str], providers: dict[str, bool]
) -> tuple[str, str]:
    if requested:
        provider = infer_provider(requested)
        if provider and providers.get(provider):
            return provider, requested
        print(
            f"[warn] Requested synthesizer '{requested}' unavailable, falling back",
            file=sys.stderr,
        )

    for provider, model in SYNTHESIZER_PRIORITY:
        if providers.get(provider):
            return provider, model

    raise RuntimeError("No synthesizer available. Set at least one API key.")


# ---------------------------------------------------------------------------
# Per-provider query functions (use cached clients)
# ---------------------------------------------------------------------------

async def query_anthropic(model: str, messages: list[dict], system: str = "") -> str:
    client = _get_anthropic()
    kwargs: dict = {"model": model, "max_tokens": 4096, "messages": messages}
    if system:
        kwargs["system"] = system
    response = await client.messages.create(**kwargs)
    return response.content[0].text


async def query_openai(model: str, messages: list[dict]) -> str:
    client = _get_openai()
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=4096,
    )
    return response.choices[0].message.content or ""


async def query_gemini(model: str, prompt: str) -> str:
    client = _get_gemini()
    response = await asyncio.to_thread(
        client.models.generate_content,
        model=model,
        contents=prompt,
    )
    return response.text


async def query_ollama(model: str, prompt: str) -> str:
    host = validate_ollama_host(
        os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    )
    client = _get_httpx()
    r = await client.post(
        f"{host}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
    )
    r.raise_for_status()
    return r.json()["response"]


async def query_model(provider: str, model: str, prompt: str) -> ModelResponse:
    try:
        messages = [{"role": "user", "content": prompt}]
        coro = (
            query_anthropic(model, messages) if provider == "anthropic"
            else query_openai(model, messages) if provider == "openai"
            else query_gemini(model, prompt) if provider == "gemini"
            else query_ollama(model, prompt) if provider == "ollama"
            else None
        )
        if coro is None:
            return ModelResponse(
                model=model, provider=provider, content="",
                error=f"Unknown provider: {provider}",
            )
        content = await asyncio.wait_for(coro, timeout=MODEL_TIMEOUT)
        return ModelResponse(model=model, provider=provider, content=content)
    except asyncio.TimeoutError:
        msg = f"timed out after {MODEL_TIMEOUT}s"
        print(f"[warn] {provider}/{model} {msg}", file=sys.stderr)
        return ModelResponse(model=model, provider=provider, content="", error=msg)
    except Exception as e:
        print(f"[warn] {provider}/{model} failed: {e}", file=sys.stderr)
        return ModelResponse(model=model, provider=provider, content="", error=str(e))


# ---------------------------------------------------------------------------
# Synthesis
# ---------------------------------------------------------------------------

SYNTHESIS_SYSTEM = (
    "You are an expert synthesizer. You will receive responses from multiple AI models "
    "to the same task. Your job is to produce a single, superior answer that:\n"
    "1. Combines the strongest insights from each response\n"
    "2. Corrects any errors or gaps you notice\n"
    "3. Is more complete and accurate than any individual response\n"
    "Respond with only the synthesized answer — no preamble about what you are doing."
)


def _truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n...[truncated at {max_chars} chars]"


def build_synthesis_prompt(original_prompt: str, responses: list[ModelResponse]) -> str:
    parts = [f"## Original Task\n{original_prompt}\n\n## Model Responses\n"]
    for i, r in enumerate(responses, 1):
        content = _truncate(r.content, MAX_RESPONSE_CHARS)
        parts.append(f"### Response {i} ({r.provider}/{r.model})\n{content}\n")
    parts.append("\n## Synthesized Answer")
    return "\n".join(parts)


async def synthesize(
    provider: str,
    model: str,
    original_prompt: str,
    responses: list[ModelResponse],
) -> str:
    synthesis_prompt = build_synthesis_prompt(original_prompt, responses)
    messages = [{"role": "user", "content": synthesis_prompt}]

    async def _run() -> str:
        if provider == "anthropic":
            return await query_anthropic(model, messages, system=SYNTHESIS_SYSTEM)
        if provider == "openai":
            full = [{"role": "system", "content": SYNTHESIS_SYSTEM}] + messages
            return await query_openai(model, full)
        if provider == "gemini":
            return await query_gemini(model, f"{SYNTHESIS_SYSTEM}\n\n{synthesis_prompt}")
        if provider == "ollama":
            return await query_ollama(model, f"{SYNTHESIS_SYSTEM}\n\n{synthesis_prompt}")
        raise ValueError(f"Unknown synthesizer provider: {provider}")

    return await asyncio.wait_for(_run(), timeout=SYNTH_TIMEOUT)


# ---------------------------------------------------------------------------
# Main ensemble logic
# ---------------------------------------------------------------------------

async def run_ensemble(
    prompt: str,
    model_list: list[tuple[str, str]],
    synth_provider: str,
    synth_model: str,
    rounds: int,
) -> EnsembleResult:
    if not model_list:
        raise RuntimeError("No models available. Check API keys / provider config.")

    all_responses: list[ModelResponse] = []
    current_prompt = prompt
    synthesis = ""

    for round_num in range(1, rounds + 1):
        label = f"[round {round_num}/{rounds}] " if rounds > 1 else ""
        print(
            f"{label}Querying {len(model_list)} models in parallel...",
            file=sys.stderr,
        )

        tasks = [query_model(p, m, current_prompt) for p, m in model_list]
        responses = list(await asyncio.gather(*tasks))
        valid = [r for r in responses if not r.error]

        if not valid:
            raise RuntimeError("All models failed. See warnings above.")

        all_responses = responses

        print(f"{label}Synthesizing with {synth_provider}/{synth_model}...", file=sys.stderr)
        synthesis = await synthesize(synth_provider, synth_model, prompt, valid)

        if round_num < rounds:
            current_prompt = (
                f"Refine and improve the following answer to the task below.\n\n"
                f"Task: {prompt}\n\nCurrent best answer:\n{synthesis}"
            )

    return EnsembleResult(
        synthesis=synthesis,
        proposer_responses=all_responses,
        synthesizer_model=f"{synth_provider}/{synth_model}",
        rounds=rounds,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="MoA: Mixture of Agents ensemble for quality improvement"
    )
    p.add_argument("--prompt", "-p", required=True, help="Task or question to query")
    p.add_argument("--models", "-m", default=None, help="Comma-separated model list")
    p.add_argument("--synthesizer", "-s", default=None, help="Synthesizer model")
    p.add_argument(
        "--rounds", "-r", type=int, default=1,
        help=f"MoA rounds, 1–{MAX_ROUNDS} (1=fast, 2=best quality)",
    )
    p.add_argument(
        "--format", choices=["text", "json"], default="text", help="Output format"
    )
    p.add_argument("--output", "-o", default=None, help="Output file path (default: stdout)")
    return p.parse_args()


async def main() -> None:
    args = parse_args()

    if not (1 <= args.rounds <= MAX_ROUNDS):
        print(f"[error] --rounds must be between 1 and {MAX_ROUNDS}", file=sys.stderr)
        sys.exit(1)

    out_path: Optional[pathlib.Path] = None
    if args.output:
        try:
            out_path = validate_output_path(args.output)
        except ValueError as e:
            print(f"[error] {e}", file=sys.stderr)
            sys.exit(1)

    providers = detect_providers()

    requested_models = (
        [m.strip() for m in args.models.split(",")] if args.models else None
    )
    model_list = await build_model_list(requested_models, providers)

    if not model_list:
        print(
            "[error] No models available. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, "
            "GEMINI_API_KEY, or OLLAMA_HOST.",
            file=sys.stderr,
        )
        sys.exit(1)

    synth_provider, synth_model = pick_synthesizer(args.synthesizer, providers)

    print(f"Proposers:    {[f'{p}/{m}' for p, m in model_list]}", file=sys.stderr)
    print(f"Synthesizer:  {synth_provider}/{synth_model}", file=sys.stderr)

    try:
        result = await run_ensemble(
            prompt=args.prompt,
            model_list=model_list,
            synth_provider=synth_provider,
            synth_model=synth_model,
            rounds=args.rounds,
        )
    finally:
        await _close_clients()

    if args.format == "json":
        output = json.dumps(
            {
                "synthesis": result.synthesis,
                "synthesizer": result.synthesizer_model,
                "rounds": result.rounds,
                "proposer_responses": [
                    {
                        "model": r.model,
                        "provider": r.provider,
                        "content": r.content,
                        "error": r.error,
                    }
                    for r in result.proposer_responses
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    else:
        output = result.synthesis

    if out_path:
        out_path.write_text(output, encoding="utf-8")
        print(f"[done] Result saved to {out_path}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    asyncio.run(main())
