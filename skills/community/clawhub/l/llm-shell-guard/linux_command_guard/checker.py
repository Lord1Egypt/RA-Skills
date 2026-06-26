from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .parser import has_command_substitution, has_dangerous_operator, parse_command
from .policy import Policy, load_policy


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str
    matched_rule: str | None = None
    base_command: str | None = None
    details: tuple[str, ...] = field(default_factory=tuple)


WRITE_LIKE_COMMANDS = {
    "rm",
    "mv",
    "cp",
    "install",
    "tee",
    "dd",
    "truncate",
    "shred",
    "wipefs",
    "mkfs",
    "mke2fs",
    "chmod",
    "chown",
    "chgrp",
    "chattr",
    "ln",
    "unlink",
    "touch",
    "sed",
    "perl",
    "python",
    "python3",
}

READ_ONLY_ALLOWLIST_GUIDANCE = (
    "Allowlist should stay small and mostly read-only. "
    "Do not allow interpreters or shell wrappers without a stricter child policy."
)


def _safe_resolve_path(value: str) -> Path | None:
    if not value:
        return None
    try:
        if value.startswith("-"):
            return None
        if value in {".", ".."}:
            return Path(value).resolve()
        if value.startswith("/") or value.startswith("./") or value.startswith("../"):
            return Path(value).resolve()
    except Exception:
        return None
    return None


def _is_under(path: Path, protected: Path) -> bool:
    try:
        path.relative_to(protected)
        return True
    except ValueError:
        return False


def _touches_protected_path(base_command: str, tokens: tuple[str, ...], policy: Policy) -> tuple[bool, str | None]:
    if base_command not in WRITE_LIKE_COMMANDS:
        return False, None
    for token in tokens[1:]:
        resolved = _safe_resolve_path(token)
        if resolved is None:
            continue
        for protected in policy.protected_paths:
            if resolved == protected or _is_under(resolved, protected):
                return True, token
    if any(tok in {">", ">>", "<", "<<", "<<<", "2>", "2>>", "&>"} for tok in tokens):
        return True, "redirection with write-like command"
    return False, None


def _contains_suspicious_shell_text(command: str) -> tuple[bool, str | None]:
    lower = command.lower()
    suspicious = [
        "bash -c",
        "sh -c",
        "zsh -c",
        "dash -c",
        "eval ",
        "exec ",
        "nohup ",
        "setsid ",
        "source ",
        "curl ",
        "wget ",
    ]
    for item in suspicious:
        if item in lower:
            return True, item.strip()
    return False, None


def evaluate_command(command: str, policy: Policy | None = None) -> Decision:
    policy = policy or load_policy()
    command = command.strip()

    if not command:
        return Decision(False, "Empty command")

    parsed = parse_command(command)
    base = parsed.base_command
    if not base:
        return Decision(False, "No executable command found")

    if has_command_substitution(command):
        return Decision(False, "Command substitution is blocked", matched_rule="command_substitution", base_command=base)

    if has_dangerous_operator(parsed.tokens):
        return Decision(False, "Shell operators and chaining are blocked", matched_rule="operators", base_command=base)

    suspicious_text, matched_text = _contains_suspicious_shell_text(command)
    if suspicious_text:
        return Decision(False, "Suspicious shell wrapper or remote-exec pattern blocked", matched_rule=matched_text, base_command=base)

    if base in policy.blocked_binaries:
        return Decision(False, "Blocked binary", matched_rule=base, base_command=base)

    if base in policy.approval_required:
        return Decision(False, "Manual approval required for high-risk binary", matched_rule=base, base_command=base)

    if policy.allowlist and base not in policy.allowlist:
        return Decision(
            False,
            "Not in allowlist",
            matched_rule=base,
            base_command=base,
            details=(READ_ONLY_ALLOWLIST_GUIDANCE,),
        )

    for bad in policy.denylist:
        if bad in command:
            return Decision(False, "Denylist match", matched_rule=bad, base_command=base)

    for pattern in policy.regex_rules:
        if re.search(pattern, command, flags=re.IGNORECASE):
            return Decision(False, "Regex rule matched", matched_rule=pattern, base_command=base)

    touches, offending = _touches_protected_path(base, parsed.tokens, policy)
    if touches:
        return Decision(False, "Protected path access blocked", matched_rule=offending, base_command=base)

    return Decision(True, "Allowed", base_command=base)
