#!/usr/bin/env python3
"""Run a local-only Ollama benchmark with a fixed fictional prompt set."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import time
from pathlib import Path
from typing import Any


THINK_LEAK_PATTERNS = (
    "<think>",
    "</think>",
    "chain of thought",
    "reasoning trace",
    "hidden reasoning",
    "internal reasoning",
    "my reasoning",
)


def load_prompts(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    prompts = data.get("prompts")
    if not isinstance(prompts, list) or not prompts:
        raise ValueError("Prompt file must contain a non-empty 'prompts' list.")
    for item in prompts:
        if not isinstance(item, dict) or not item.get("id") or not item.get("prompt"):
            raise ValueError("Each prompt must contain at least 'id' and 'prompt'.")
    return prompts


def has_think_leak(text: str) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in THINK_LEAK_PATTERNS)


def format_passes(output: str, expected_format: str) -> bool:
    stripped = output.strip()
    if not stripped:
        return False
    if expected_format == "json":
        try:
            json.loads(stripped)
            return True
        except json.JSONDecodeError:
            return False
    if expected_format == "markdown_bullets":
        return any(line.lstrip().startswith(("-", "*")) for line in stripped.splitlines())
    if expected_format == "markdown_sections":
        return any(line.lstrip().startswith("#") for line in stripped.splitlines())
    return True


def run_ollama(model: str, prompt: str, timeout: int) -> tuple[bool, str, str, float]:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.monotonic() - started
        return False, exc.stdout or "", f"timeout after {timeout}s", elapsed
    except FileNotFoundError:
        elapsed = time.monotonic() - started
        return False, "", "ollama command not found", elapsed

    elapsed = time.monotonic() - started
    ok = completed.returncode == 0
    error = completed.stderr.strip()
    return ok, completed.stdout, error, elapsed


def build_records(models: list[str], prompts: list[dict[str, Any]], rounds: int, timeout: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for round_number in range(1, rounds + 1):
        for model in models:
            for prompt in prompts:
                ok, output, error, elapsed = run_ollama(model, prompt["prompt"], timeout)
                expected_format = str(prompt.get("expected_format", "plain_text"))
                records.append(
                    {
                        "round": round_number,
                        "model": model,
                        "prompt_id": prompt["id"],
                        "prompt_title": prompt.get("title", prompt["id"]),
                        "category": prompt.get("category", "unknown"),
                        "expected_format": expected_format,
                        "success": ok,
                        "duration_seconds": round(elapsed, 3),
                        "output_chars": len(output),
                        "format_pass": format_passes(output, expected_format),
                        "think_leak": has_think_leak(output),
                        "error": error,
                        "output": output.strip(),
                    }
                )
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a local Ollama two-round model benchmark.")
    parser.add_argument("--models", nargs="+", required=True, help="Installed local Ollama model names.")
    parser.add_argument("--prompts", required=True, type=Path, help="Path to prompt JSON file.")
    parser.add_argument("--rounds", type=int, default=2, help="Benchmark rounds. Use 2 for replacement decisions.")
    parser.add_argument("--timeout", type=int, default=180, help="Timeout per prompt in seconds.")
    parser.add_argument("--output", required=True, type=Path, help="Output benchmark JSON path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.rounds < 1:
        raise SystemExit("--rounds must be at least 1")

    prompts = load_prompts(args.prompts)
    records = build_records(args.models, prompts, args.rounds, args.timeout)
    payload = {
        "version": "1.5.0",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "local_only": True,
        "rounds_requested": args.rounds,
        "models": args.models,
        "prompt_count": len(prompts),
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote benchmark results to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

