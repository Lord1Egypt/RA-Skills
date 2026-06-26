#!/usr/bin/env python3
"""Inventory possible independent reviewer model channels.

This script does not print secret values and does not call the network.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Candidate:
    name: str
    kind: str
    available: bool
    evidence: List[str]
    model_hint: Optional[str] = None
    notes: str = ""


def env_present(name: str) -> bool:
    return bool(os.environ.get(name))


def env_evidence(*names: str) -> List[str]:
    return [name for name in names if env_present(name)]


def command_candidate(command: str, note: str) -> Candidate:
    path = shutil.which(command)
    return Candidate(
        name=command,
        kind="cli",
        available=path is not None,
        evidence=[path] if path else [],
        notes=note,
    )


def route_from_spec(spec: Dict[str, object]) -> Candidate:
    name = str(spec.get("name") or "custom-route")
    kind = str(spec.get("kind") or "api")
    command = str(spec.get("command") or "")
    envs = [str(item) for item in spec.get("env", [])]
    require = str(spec.get("requires") or "any")
    model_env = str(spec.get("model_env") or "")
    model_hint = str(spec.get("model") or os.environ.get(model_env, "") or "") or None
    notes = str(spec.get("notes") or "Custom review route.")

    evidence: List[str] = []
    available = False
    if command:
        path = shutil.which(command)
        if path:
            evidence.append(path)
            available = True

    present_envs = env_evidence(*envs)
    evidence.extend(present_envs)
    if envs:
        if require == "all":
            available = available or len(present_envs) == len(envs)
        else:
            available = available or bool(present_envs)

    return Candidate(
        name=name,
        kind=kind,
        available=available,
        evidence=evidence,
        model_hint=model_hint,
        notes=notes,
    )


def extract_route_specs(loaded: object) -> List[Dict[str, object]]:
    if isinstance(loaded, list):
        return [item for item in loaded if isinstance(item, dict)]
    if isinstance(loaded, dict):
        routes = loaded.get("routes", [])
        return [item for item in routes if isinstance(item, dict)]
    return []


def load_route_specs(config_path: str) -> List[Dict[str, object]]:
    specs: List[Dict[str, object]] = []
    raw_json = os.environ.get("CODE_AUDIT_REVIEW_ROUTES_JSON", "")
    if raw_json:
        loaded = json.loads(raw_json)
        specs.extend(extract_route_specs(loaded))

    if not config_path:
        default = Path(__file__).resolve().parents[1] / "review_routes.json"
        config_path = str(default) if default.exists() else ""
    if config_path:
        loaded = json.loads(Path(config_path).read_text(encoding="utf-8"))
        specs.extend(extract_route_specs(loaded))
    return specs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--current-model", default="", help="Development model, if known.")
    parser.add_argument("--config", default="", help="JSON file with custom review routes.")
    args = parser.parse_args()
    current_model = args.current_model.strip().lower()

    candidates = [
        Candidate(
            name="openai-compatible-api",
            kind="api",
            available=bool(env_evidence("OPENAI_API_KEY", "OPENAI_BASE_URL")),
            evidence=env_evidence("OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL"),
            model_hint=os.environ.get("OPENAI_MODEL"),
            notes="Verify selected model is not the development model.",
        ),
        Candidate(
            name="anthropic-api",
            kind="api",
            available=env_present("ANTHROPIC_API_KEY"),
            evidence=env_evidence("ANTHROPIC_API_KEY", "ANTHROPIC_MODEL"),
            model_hint=os.environ.get("ANTHROPIC_MODEL"),
            notes="Prefer only if repo policy allows external code review.",
        ),
        Candidate(
            name="gemini-api",
            kind="api",
            available=bool(env_evidence("GEMINI_API_KEY", "GOOGLE_API_KEY")),
            evidence=env_evidence("GEMINI_API_KEY", "GOOGLE_API_KEY", "GEMINI_MODEL"),
            model_hint=os.environ.get("GEMINI_MODEL"),
            notes="Good cross-family candidate when configured.",
        ),
        Candidate(
            name="deepseek-api",
            kind="api",
            available=bool(env_evidence("DEEPSEEK_API_KEY", "DEEPSEEK_BASE_URL", "DEEPSEEK_MODEL")),
            evidence=env_evidence("DEEPSEEK_API_KEY", "DEEPSEEK_BASE_URL", "DEEPSEEK_MODEL"),
            model_hint=os.environ.get("DEEPSEEK_MODEL"),
            notes="Custom DeepSeek route; verify policy and exact model before external review.",
        ),
        Candidate(
            name="hermes-provider",
            kind="api",
            available=bool(env_evidence("HERMES_API_KEY", "HERMES_API_BASE_URL", "HERMES_BASE_URL", "HERMES_MODEL")),
            evidence=env_evidence("HERMES_API_KEY", "HERMES_API_BASE_URL", "HERMES_BASE_URL", "HERMES_MODEL"),
            model_hint=os.environ.get("HERMES_MODEL"),
            notes="Hermes/custom provider route; use local config to identify exact model.",
        ),
        Candidate(
            name="openrouter-api",
            kind="api",
            available=bool(env_evidence("OPENROUTER_API_KEY", "OPENROUTER_MODEL")),
            evidence=env_evidence("OPENROUTER_API_KEY", "OPENROUTER_MODEL"),
            model_hint=os.environ.get("OPENROUTER_MODEL"),
            notes="OpenRouter route; verify selected model is not the development model.",
        ),
        Candidate(
            name="kimi-api",
            kind="api",
            available=bool(env_evidence("KIMI_API_KEY", "KIMI_API_BASE_URL")),
            evidence=env_evidence("KIMI_API_KEY", "KIMI_API_BASE_URL", "KIMI_MODEL"),
            model_hint=os.environ.get("KIMI_MODEL"),
            notes="Check AGENTS.md; some repos restrict Kimi to frontend design advice.",
        ),
        Candidate(
            name="mistral-api",
            kind="api",
            available=env_present("MISTRAL_API_KEY"),
            evidence=env_evidence("MISTRAL_API_KEY", "MISTRAL_MODEL"),
            model_hint=os.environ.get("MISTRAL_MODEL"),
            notes="Use only if adequate for the audit risk.",
        ),
        command_candidate("claude", "CLI route may still be same-family; disclose correlation risk."),
        command_candidate("gemini", "CLI candidate if installed and authenticated."),
        command_candidate("ollama", "Local candidate; confirm model quality/context is sufficient."),
    ]
    candidates.extend(route_from_spec(spec) for spec in load_route_specs(args.config))

    for candidate in candidates:
        hint = (candidate.model_hint or "").strip().lower()
        if current_model and hint and hint == current_model:
            candidate.notes = "Not independent: model hint matches development model exactly."

    print(
        json.dumps(
            {
                "current_model": args.current_model or None,
                "available": [c.name for c in candidates if c.available],
                "available_review_routes": [c.name for c in candidates if c.available],
                "candidates": [asdict(c) for c in candidates],
                "secret_values_printed": False,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
