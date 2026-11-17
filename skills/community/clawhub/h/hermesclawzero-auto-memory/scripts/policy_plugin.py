"""
policy_plugin.py — Hermes Agent Policy Engine Plugin v2

Drop this file into ~/.hermes/plugins/ to activate runtime policy enforcement.
When the Hermes Agent PR is merged, this becomes native.

Includes: Policy IDs, Schema Version (2), Audit Logging, Priority-Weighted Resolution.
"""

import datetime
import fnmatch
import json
import logging
import os
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:
    yaml = None

# ── Schema version ────────────────────────────────────────────────────────
POLICY_SCHEMA_VERSION = 2

# ── Logging ───────────────────────────────────────────────────────────────
_POLICY_LOG_PATH: Optional[str] = None


def _get_log_path() -> str:
    global _POLICY_LOG_PATH
    if _POLICY_LOG_PATH is None:
        hermes_home = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
        _POLICY_LOG_PATH = os.path.join(hermes_home, "policy_audit.jsonl")
    return _POLICY_LOG_PATH


def _log_decision(
    decision: str,       # "blocked" | "allowed" | "prompted"
    tool: str,
    action: str,
    policy_id: str,
    reason: str,
    rule: str = "",
):
    """Append one audit line to ~/.hermes/policy_audit.jsonl."""
    entry = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "decision": decision,
        "tool": tool,
        "action": action[:200],
        "policy_id": policy_id or "-",
        "reason": reason,
        "rule": rule[:200],
        "schema_version": POLICY_SCHEMA_VERSION,
    }
    try:
        log_path = _get_log_path()
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass  # Logging must never block execution


def read_audit_log(lines: int = 50) -> list[dict]:
    """Read last N entries from policy_audit.jsonl."""
    log_path = _get_log_path()
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, encoding="utf-8") as f:
            all_lines = [l.strip() for l in f if l.strip()]
        result = []
        for l in all_lines[-lines:]:
            try:
                result.append(json.loads(l))
            except json.JSONDecodeError:
                continue
        return result
    except Exception:
        return []


# ── Priority order ────────────────────────────────────────────────────────
_PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


# ── Policy Engine ─────────────────────────────────────────────────────────

class PolicyEngine:
    """Evaluates tool calls against registered policies."""

    def __init__(self):
        self._policies: list[dict] = []
        self._loaded = False

    def load_from_skills(self, skills_dir: str | Path | None = None) -> int:
        """Scan all installed skills for enforce: frontmatter and register policies."""
        if yaml is None:
            return 0

        if skills_dir is None:
            hermes_home = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
            skills_dir = Path(hermes_home) / "skills"

        skills_dir = Path(skills_dir)
        if not skills_dir.exists():
            return 0

        count = 0
        for skill_md in skills_dir.rglob("SKILL.md"):
            if ".git" in str(skill_md) or "__pycache__" in str(skill_md):
                continue
            try:
                raw = skill_md.read_text(encoding="utf-8")
                if not raw.startswith("---"):
                    continue
                parts = raw.split("---", 2)
                if len(parts) < 3:
                    continue
                fm = yaml.safe_load(parts[1])
                if not isinstance(fm, dict):
                    continue
                rules = fm.get("enforce", [])
                if rules:
                    self._policies.extend(rules)
                    count += len(rules)
            except Exception:
                continue

        self._loaded = True
        return count

    def evaluate(self, tool: str, action: str) -> dict:
        """Evaluate a tool call against registered policies.

        Returns:
            {"allow": True, "reason": "", "policy_id": ""}  — allowed
            {"allow": False, "reason": "...", "policy_id": "..."} — blocked
            {"allow": None, "reason": "...", "policy_id": "..."} — needs prompt
        """
        if not self._loaded:
            self.load_from_skills()

        best = {"allow": True, "reason": "", "policy_id": "", "_priority": 99, "_action_score": 2}
        for p in self._policies:
            pol = p.get("policy", {})
            tool_match = pol.get("tool", "") in ("*", tool) or tool in pol.get("tool", "").split("|")
            if not tool_match:
                continue
            pattern = pol.get("pattern", "*")
            pattern_match = any(
                fnmatch.fnmatch(action, pat.strip())
                for pat in pattern.split("|")
            )
            if not pattern_match:
                continue
            prio = _PRIORITY_ORDER.get(p.get("priority", "medium"), 99)
            act = pol.get("action", "allow")
            action_score = {"deny": 0, "prompt": 1, "allow": 2, "always": 3}.get(act, 2)
            if prio < best["_priority"] or (prio == best["_priority"] and action_score < best["_action_score"]):
                best = {
                    "allow": None if act == "prompt" else (act in ("allow", "always")),
                    "reason": pol.get("reason", ""),
                    "policy_id": p.get("id", ""),
                    "_priority": prio,
                    "_action_score": action_score,
                }
        return {"allow": best["allow"], "reason": best["reason"], "policy_id": best["policy_id"]}


# ── Singleton ──────────────────────────────────────────────────────────────

_engine: Optional[PolicyEngine] = None


def get_engine() -> PolicyEngine:
    global _engine
    if _engine is None:
        _engine = PolicyEngine()
    return _engine


# ── Hermes Plugin Hook ────────────────────────────────────────────────────

def get_pre_tool_call_block_message(
    function_name: str,
    function_args: dict[str, Any],
    **kwargs,
) -> str | None:
    """Check if a tool call should be blocked by policy.

    Called by Hermes Agent's tool dispatch pipeline before every execution.
    Returns a block message (str) if the action is denied, None if allowed.
    """
    engine = get_engine()

    action = function_name
    if function_name in ("terminal", "exec"):
        cmd = function_args.get("command", "") or function_args.get("cmd", "")
        action = f"{function_name}:{cmd[:200]}"
    elif function_name in ("write_file", "patch", "delete", "edit", "apply_patch"):
        path = function_args.get("path", "") or function_args.get("file_path", "")
        action = f"{function_name}:{path}"
    elif function_name == "web_fetch":
        url = function_args.get("url", "") or function_args.get("urls", "")
        action = f"{function_name}:{str(url)[:200]}"

    result = engine.evaluate(function_name, action)

    if result["allow"] is False:
        reason = result.get("reason", "Blocked by policy")
        pid = result.get("policy_id", "-")
        _log_decision("blocked", function_name, action, pid, reason)
        return f"⛔ [{pid}] Policy blocked: {reason}"

    # prompt: return a special prefix Hermes routes to approval flow
    if result["allow"] is None:
        pid = result.get("policy_id", "-")
        reason = result.get("reason", "Needs approval")
        _log_decision("prompted", function_name, action, pid, reason)
        return f"⚠️ [{pid}] Policy requires approval: {reason}"

    # Only log "allowed" for dangerous tool categories to avoid flooding
    if result["allow"] is True and function_name in ("terminal", "exec", "write_file", "patch", "delete", "edit", "apply_patch", "docker", "git"):
        _log_decision("allowed", function_name, action, "", "")
    elif result["allow"] is True:
        pass  # skip audit for safe tools (read, search, list, etc.)

    return None  # Allowed — Hermes proceeds normally
