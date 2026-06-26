#!/usr/bin/env python3
"""
Multi-layer model detector.

Runs a set of probes, each returning zero or more DetectionResult(s), and
prints a consolidated report. Used as a diagnostic ("what is the agent
actually using right now?") and as a building block for the tailer.

Each probe should be cheap; no network calls.

Usage:
    python3 scripts/detect_model.py                 # pretty table
    python3 scripts/detect_model.py --json          # machine-readable

Probes shipped:
    env          — ANTHROPIC_MODEL / OPENAI_MODEL / CLAUDE_MODEL / etc.
    openclaw     — latest ~/.openclaw/agents/main/sessions/*.jsonl
    claude-code  — latest ~/.claude/projects/*/sessions/*.jsonl
    claude-settings — ~/.claude/settings.json
    usage-log    — most recent entry in ~/.cost-watchdog/usage.jsonl
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
import usage_log  # noqa: E402


HOME = Path.home()
CONFIDENCE_ORDER = {"high": 3, "medium": 2, "low": 1}


@dataclass
class DetectionResult:
    source: str
    provider: Optional[str]
    model: Optional[str]
    confidence: str         # "high" | "medium" | "low"
    note: str = ""          # freeform — timestamp, session id, etc.


# ---------------------------------------------------------------------------
# Probes
# ---------------------------------------------------------------------------

_ENV_VARS = [
    # (env_var, provider_hint)
    ("ANTHROPIC_MODEL", "anthropic"),
    ("CLAUDE_MODEL", "anthropic"),
    ("OPENAI_MODEL", "openai"),
    ("LITELLM_MODEL", None),
    ("OPENROUTER_MODEL", "openrouter"),
    ("COST_WATCHDOG_MODEL", None),
]


def probe_env() -> List[DetectionResult]:
    out = []
    for var, provider in _ENV_VARS:
        val = os.environ.get(var)
        if val:
            out.append(DetectionResult(
                source=f"env/{var}",
                provider=provider,
                model=val,
                confidence="medium",
                note="configured; not necessarily the last-used model",
            ))
    return out


def _latest_session_file(folder: Path) -> Optional[Path]:
    """Return the most recently modified *.jsonl that isn't a deleted/reset variant."""
    if not folder.exists():
        return None
    candidates = [
        p for p in folder.glob("*.jsonl")
        if "deleted" not in p.name and "reset" not in p.name
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _scan_jsonl_backwards(path: Path, max_bytes: int = 2_000_000) -> Iterable[dict]:
    """
    Yield parsed JSON objects from a JSONL file, newest first.
    Reads at most the last `max_bytes` to avoid slurping huge files.
    """
    try:
        size = path.stat().st_size
        with path.open("rb") as f:
            if size > max_bytes:
                f.seek(size - max_bytes)
                f.readline()  # discard partial line
            data = f.read().decode("utf-8", errors="replace")
    except OSError:
        return
    for line in reversed(data.splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def probe_openclaw() -> List[DetectionResult]:
    sessions_dir = HOME / ".openclaw" / "agents" / "main" / "sessions"
    path = _latest_session_file(sessions_dir)
    if not path:
        return []

    last_assistant_model = None
    last_assistant_provider = None
    last_model_change = None
    session_id = path.stem

    for event in _scan_jsonl_backwards(path):
        if event.get("type") == "message":
            msg = event.get("message")
            if isinstance(msg, str):
                try:
                    msg = json.loads(msg)
                except json.JSONDecodeError:
                    continue
            if isinstance(msg, dict) and msg.get("role") == "assistant":
                last_assistant_model = msg.get("model")
                last_assistant_provider = msg.get("provider")
                if last_assistant_model:
                    break
        elif event.get("type") == "model_change":
            if last_model_change is None:
                last_model_change = (event.get("provider"), event.get("modelId"))

    out = []
    if last_assistant_model:
        out.append(DetectionResult(
            source="openclaw/session (last assistant turn)",
            provider=last_assistant_provider,
            model=last_assistant_model,
            confidence="high",
            note=f"session={session_id[:8]}...",
        ))
    elif last_model_change:
        provider, model = last_model_change
        out.append(DetectionResult(
            source="openclaw/session (model_change)",
            provider=provider,
            model=model,
            confidence="high",
            note=f"session={session_id[:8]}... (no assistant turn yet)",
        ))
    return out


def probe_claude_code() -> List[DetectionResult]:
    """
    Claude Code stores per-project session jsonl under
    ~/.claude/projects/<encoded-path>/sessions/<id>.jsonl
    """
    projects_root = HOME / ".claude" / "projects"
    if not projects_root.exists():
        return []

    # Find the latest session across all projects.
    candidates = []
    for project in projects_root.iterdir():
        if not project.is_dir():
            continue
        sessions = project / "sessions"
        if not sessions.exists():
            continue
        latest = _latest_session_file(sessions)
        if latest:
            candidates.append(latest)
    if not candidates:
        return []
    path = max(candidates, key=lambda p: p.stat().st_mtime)

    # Claude Code session schema has events with a `message` field that
    # includes model info on assistant turns.
    for event in _scan_jsonl_backwards(path):
        msg = event.get("message") if isinstance(event, dict) else None
        if isinstance(msg, str):
            try:
                msg = json.loads(msg)
            except json.JSONDecodeError:
                msg = None
        if isinstance(msg, dict):
            model = msg.get("model")
            if model:
                return [DetectionResult(
                    source="claude-code/session",
                    provider="anthropic",
                    model=model,
                    confidence="high",
                    note=f"project={path.parent.parent.name}",
                )]
    return []


def probe_claude_settings() -> List[DetectionResult]:
    path = HOME / ".claude" / "settings.json"
    if not path.exists():
        return []
    try:
        body = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    model = body.get("model")
    if not model:
        return []
    return [DetectionResult(
        source="claude-code/settings.json",
        provider="anthropic",
        model=model,
        confidence="medium",
        note="configured default; may be overridden at runtime",
    )]


def probe_usage_log() -> List[DetectionResult]:
    recent = usage_log.read_recent(limit=1)
    if not recent:
        return []
    entry = recent[0]
    model = entry.get("model")
    if not model:
        return []
    return [DetectionResult(
        source=f"usage-log/{entry.get('source', 'unknown')}",
        provider=entry.get("provider"),
        model=model,
        confidence="high",
        note=f"last call {_fmt_age(entry.get('ts', 0))} ago",
    )]


def _fmt_age(ts: float) -> str:
    import time
    age = time.time() - ts
    if age < 0:
        return "?"
    for unit, seconds in (("d", 86400), ("h", 3600), ("m", 60)):
        if age >= seconds:
            return f"{age/seconds:.0f}{unit}"
    return f"{age:.0f}s"


PROBES = [
    ("env", probe_env),
    ("openclaw", probe_openclaw),
    ("claude-code/session", probe_claude_code),
    ("claude-code/settings", probe_claude_settings),
    ("usage-log", probe_usage_log),
]


def detect_all() -> List[DetectionResult]:
    results: List[DetectionResult] = []
    for _, probe in PROBES:
        try:
            results.extend(probe())
        except Exception as e:  # probes must never crash the report
            results.append(DetectionResult(
                source=f"{probe.__name__}/ERROR",
                provider=None, model=None,
                confidence="low",
                note=str(e),
            ))
    return results


def best_guess(results: List[DetectionResult]) -> Optional[DetectionResult]:
    if not results:
        return None
    ranked = sorted(
        results,
        key=lambda r: (CONFIDENCE_ORDER.get(r.confidence, 0), r.source),
        reverse=True,
    )
    return ranked[0]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _render_table(results: List[DetectionResult]) -> str:
    if not results:
        return "No model detected from any source."
    w_source = max(len(r.source) for r in results)
    w_model = max(len(str(r.model)) for r in results)
    w_provider = max(len(str(r.provider or "")) for r in results)
    header = f"{'SOURCE':<{w_source}}  {'PROVIDER':<{w_provider}}  {'MODEL':<{w_model}}  CONF   NOTE"
    lines = [header, "-" * len(header)]
    for r in results:
        lines.append(
            f"{r.source:<{w_source}}  "
            f"{(r.provider or ''):<{w_provider}}  "
            f"{(r.model or ''):<{w_model}}  "
            f"{r.confidence:<5}  {r.note}"
        )
    guess = best_guess(results)
    if guess:
        lines.append("")
        lines.append(f"Best guess: {guess.provider or '?'} / {guess.model}  [via {guess.source}]")
    return "\n".join(lines)


def main() -> int:
    args = sys.argv[1:]
    results = detect_all()
    if "--json" in args:
        payload = {
            "results": [asdict(r) for r in results],
            "best_guess": asdict(best_guess(results)) if best_guess(results) else None,
        }
        print(json.dumps(payload, indent=2))
    else:
        print(_render_table(results))
    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())
