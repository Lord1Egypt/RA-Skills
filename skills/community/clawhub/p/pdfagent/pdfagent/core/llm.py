from __future__ import annotations

import json
import shlex
from typing import Any

from .exec import ExternalCommandError, run_cmd


class LLMError(RuntimeError):
    pass


def generate_text(
    *,
    provider: str,
    prompt: str,
    cmd: str | None = None,
    model: str | None = None,
) -> str:
    if provider == "none":
        raise LLMError("LLM provider is disabled")
    if provider == "command":
        if not cmd:
            raise LLMError("--llm-cmd is required for provider=command")
        return _run_command_text(cmd, prompt)
    if provider == "ollama":
        if not model:
            raise LLMError("--model is required for provider=ollama")
        return _run_ollama_text(model, prompt)

    raise LLMError(f"Unsupported LLM provider: {provider}")


def generate_plan(
    *,
    provider: str,
    prompt: str,
    cmd: str | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    if provider == "none":
        raise LLMError("LLM provider is disabled")
    if provider == "command":
        if not cmd:
            raise LLMError("--llm-cmd is required for provider=command")
        return _run_command_llm(cmd, prompt)
    if provider == "ollama":
        if not model:
            raise LLMError("--model is required for provider=ollama")
        return _run_ollama(model, prompt)

    raise LLMError(f"Unsupported LLM provider: {provider}")


def _run_command_llm(cmd: str, prompt: str) -> dict[str, Any]:
    if "{prompt}" in cmd:
        rendered = cmd.replace("{prompt}", json.dumps(prompt))
        args = shlex.split(rendered)
        output = run_cmd(args)
    else:
        args = shlex.split(cmd)
        output = run_cmd(args, input_text=prompt)

    return _parse_json(output)


def _run_command_text(cmd: str, prompt: str) -> str:
    if "{prompt}" in cmd:
        rendered = cmd.replace("{prompt}", json.dumps(prompt))
        args = shlex.split(rendered)
        return run_cmd(args)
    args = shlex.split(cmd)
    return run_cmd(args, input_text=prompt)


def _run_ollama(model: str, prompt: str) -> dict[str, Any]:
    args = ["ollama", "run", model]
    output = run_cmd(args, input_text=prompt)
    return _parse_json(output)


def _run_ollama_text(model: str, prompt: str) -> str:
    args = ["ollama", "run", model]
    return run_cmd(args, input_text=prompt)


def _parse_json(text: str) -> dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise LLMError("LLM output was not valid JSON") from exc
