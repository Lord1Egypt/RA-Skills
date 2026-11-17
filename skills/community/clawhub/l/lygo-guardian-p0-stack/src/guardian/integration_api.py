"""Guardian integration API — no network. Gate untrusted skill text before trust."""

from .p0_kernel_core import validate_with_understanding


def validate_decision(context: dict, candidate: dict) -> dict:
    content = candidate.get("content", "")
    return validate_with_understanding(content, context)


def guardian_wrap(fn):
    def wrapped(context, *args, **kwargs):
        raw = fn(context, *args, **kwargs)
        verdict = validate_decision(context, {"content": raw})
        action = verdict.get("action", "allow")
        if action == "allow":
            return raw
        if action == "flag":
            note = verdict.get("understanding") or "Guardian flagged this content as risky."
            return f"{raw}\n\n[LYGO Guardian Note]: {note}"
        if action == "isolate":
            return "[BLOCKED BY LYGO GUARDIAN: content failed Nano-Kernel validation]"
        return "[LYGO GUARDIAN REQUESTS REVIEW BEFORE SENDING THIS]"

    return wrapped