#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass

ZERO_LLM_PATTERNS = [
    r"\bpet all\b",
    r"\bpet my gotchis\b",
    r"\b53 gotchis\b",
    r"\bcooldown\b",
    r"\bcron\b",
    r"\bdeterministic\b",
    r"\bscript\b",
]

WALLET_PATTERNS = [
    r"\bwallet\b",
    r"\bsend\b",
    r"\btransfer\b",
    r"\bswap\b",
    r"\bbroadcast\b",
    r"\bsign\b",
    r"\bapprove\b",
    r"\btreasury\b",
    r"\beth\b",
    r"\busdc\b",
]

CODE_PATTERNS = [
    r"\bcode\b",
    r"\bscript\b",
    r"\bbug\b",
    r"\bfix\b",
    r"\bpatch\b",
    r"\brefactor\b",
    r"\brepo\b",
    r"\bskill\b",
]

VISION_PATTERNS = [
    r"\bimage\b",
    r"\bscreenshot\b",
    r"\bvisual\b",
    r"\blogo\b",
    r"\bsvg\b",
]

LONG_CONTEXT_PATTERNS = [
    r"\bcompare\b.*\bdocs\b",
    r"\blong context\b",
    r"\bmultiple docs\b",
    r"\bsynthesize\b",
    r"\bdeep read\b",
]

@dataclass
class RouteDecision:
    route: str
    fallback: str | None
    risk: str
    task_type: str
    reason: str


def matches_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def detect_task_type(text: str, explicit: str | None) -> str:
    if explicit and explicit != "auto":
        return explicit
    if matches_any(text, ZERO_LLM_PATTERNS):
        return "deterministic"
    if matches_any(text, WALLET_PATTERNS):
        return "wallet"
    if matches_any(text, VISION_PATTERNS):
        return "vision"
    if matches_any(text, LONG_CONTEXT_PATTERNS):
        return "long-context"
    if matches_any(text, CODE_PATTERNS):
        return "code"
    return "chat"


def route_message(text: str, task_type: str, high_stakes: bool, allow_zero_llm: bool) -> RouteDecision:
    if task_type == "deterministic" and allow_zero_llm:
        return RouteDecision(
            route="zero-llm",
            fallback=None,
            risk="low",
            task_type=task_type,
            reason="Matched a deterministic workflow that should bypass LLM usage.",
        )

    if high_stakes:
        return RouteDecision(
            route="bankr/claude-opus-4.6",
            fallback="bankr/claude-sonnet-4.5",
            risk="high",
            task_type=task_type,
            reason="Explicit high-stakes escalation; prioritize caution over cost.",
        )

    if task_type == "wallet":
        return RouteDecision(
            route="bankr/claude-sonnet-4.5",
            fallback="bankr/claude-opus-4.6",
            risk="medium",
            task_type=task_type,
            reason="Routine wallet or treasury operation; use the cheapest model with strong enough judgment.",
        )

    if task_type == "code":
        return RouteDecision(
            route="bankr/gpt-5.2-codex",
            fallback="bankr/claude-sonnet-4.5",
            risk="medium",
            task_type=task_type,
            reason="Coding-heavy request; use the coding specialist route.",
        )

    if task_type == "vision":
        return RouteDecision(
            route="bankr/gemini-3-flash",
            fallback="bankr/gemini-3-pro",
            risk="medium",
            task_type=task_type,
            reason="Vision or visual triage request; use the multimodal route.",
        )

    if task_type == "long-context":
        return RouteDecision(
            route="bankr/gemini-3-pro",
            fallback="bankr/claude-sonnet-4.5",
            risk="medium",
            task_type=task_type,
            reason="Long-context synthesis request; use the long-context route.",
        )

    if len(text.split()) <= 40:
        return RouteDecision(
            route="bankr/minimax-m2.5",
            fallback="bankr/claude-sonnet-4.5",
            risk="low",
            task_type=task_type,
            reason="Low-risk lightweight request; use the cheapest adequate route.",
        )

    return RouteDecision(
        route="bankr/claude-sonnet-4.5",
        fallback="bankr/minimax-m2.5",
        risk="medium",
        task_type=task_type,
        reason="Default general-reasoning route for normal aaigotchi work.",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Route a message to the right Bankr model.")
    parser.add_argument("--text", required=True, help="Message text to classify")
    parser.add_argument("--task-type", default="auto", choices=["auto", "chat", "code", "wallet", "vision", "long-context", "deterministic"], help="Optional explicit task type")
    parser.add_argument("--high-stakes", action="store_true", help="Force the high-stakes route")
    parser.add_argument("--allow-zero-llm", choices=["true", "false"], default="true", help="Allow deterministic zero-LLM routing")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    text = args.text.strip().lower()
    task_type = detect_task_type(text, args.task_type)
    decision = route_message(text, task_type, args.high_stakes, args.allow_zero_llm == "true")

    if args.json:
        print(json.dumps(asdict(decision), indent=2))
    else:
        print(f"route: {decision.route}")
        print(f"fallback: {decision.fallback or 'none'}")
        print(f"risk: {decision.risk}")
        print(f"task_type: {decision.task_type}")
        print(f"reason: {decision.reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
