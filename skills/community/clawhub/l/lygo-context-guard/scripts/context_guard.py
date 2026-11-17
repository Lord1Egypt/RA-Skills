#!/usr/bin/env python3
"""
LYGO Context Guard — token budget, compact, redact, preflight.

Every agent hits context limits. This skill is the pre-flight gate before
stuffing tool dumps, logs, files, or long chats into a pay-to-go model.

Pure stdlib. No network. No subprocess.
Writes only under skill state/ with --i-consent.

Signature: Delta9Phi963-CONTEXT-GUARD-v1.0.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIG = "Delta9Phi963-CONTEXT-GUARD-v1.0.0"
VERSION = "1.0.0"
HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
STATE = SKILL / "state"

# Rough OpenAI-style heuristic (English-ish). Not a tokenizer; good enough for budgets.
CHARS_PER_TOKEN = 4.0
WORDS_PER_TOKEN = 0.75

# Secret / credential patterns (redact, never log raw)
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("openai_sk", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("anthropic_key", re.compile(r"\bsk-ant-[A-Za-z0-9\-_]{20,}\b")),
    ("github_pat", re.compile(r"\bghp_[A-Za-z0-9]{20,}\b")),
    ("github_fine", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("aws_access", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("aws_secret", re.compile(r"(?i)aws_secret_access_key\s*[=:]\s*['\"]?([A-Za-z0-9/+=]{30,})")),
    ("bearer", re.compile(r"(?i)bearer\s+[A-Za-z0-9\-._~+/]+=*")),
    ("generic_api_key", re.compile(r"(?i)(api[_-]?key|access[_-]?token|secret[_-]?key)\s*[=:]\s*['\"]?([^\s'\"]{16,})")),
    ("private_key_block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b")),
    ("password_assign", re.compile(r"(?i)(password|passwd|pwd)\s*[=:]\s*['\"]?([^\s'\"]{6,})")),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def estimate_tokens(text: str) -> dict[str, Any]:
    """Dual heuristic: char/4 and words/0.75; report max as conservative budget."""
    if not text:
        return {
            "chars": 0,
            "words": 0,
            "tokens_char_heuristic": 0,
            "tokens_word_heuristic": 0,
            "tokens_estimate": 0,
            "method": "empty",
        }
    chars = len(text)
    words = len(re.findall(r"\S+", text))
    t_char = int(round(chars / CHARS_PER_TOKEN))
    t_word = int(round(words / WORDS_PER_TOKEN)) if words else 0
    # conservative for budgeting: take the higher estimate
    est = max(t_char, t_word)
    return {
        "chars": chars,
        "words": words,
        "tokens_char_heuristic": t_char,
        "tokens_word_heuristic": t_word,
        "tokens_estimate": est,
        "method": f"max(chars/{CHARS_PER_TOKEN}, words/{WORDS_PER_TOKEN})",
        "note": "Heuristic only — not model-exact. Use as budget guardrail.",
    }


def redact_secrets(text: str) -> dict[str, Any]:
    hits: list[dict[str, Any]] = []
    out = text
    for name, rx in SECRET_PATTERNS:
        found = list(rx.finditer(out))
        if not found:
            continue
        hits.append({"pattern": name, "count": len(found)})
        out = rx.sub(f"[REDACTED:{name}]", out)
    return {
        "ok": True,
        "redacted": out,
        "hits": hits,
        "total_hits": sum(h["count"] for h in hits),
        "changed": out != text,
    }


def compact_text(
    text: str,
    *,
    max_chars: int = 12000,
    keep_head: int = 4000,
    keep_tail: int = 2000,
    dedupe_lines: bool = True,
    strip_blank_runs: bool = True,
) -> dict[str, Any]:
    """Deterministic compaction — no LLM required."""
    original = text
    t = text.replace("\r\n", "\n").replace("\r", "\n")

    if strip_blank_runs:
        t = re.sub(r"\n{3,}", "\n\n", t)

    if dedupe_lines:
        lines = t.split("\n")
        seen: set[str] = set()
        kept: list[str] = []
        dropped = 0
        for ln in lines:
            key = ln.strip()
            if key and key in seen and len(key) > 40:
                dropped += 1
                continue
            if key:
                seen.add(key)
            kept.append(ln)
        t = "\n".join(kept)
    else:
        dropped = 0

    truncated = False
    if max_chars > 0 and len(t) > max_chars:
        # keep head + tail with middle map
        head_n = min(keep_head, max_chars // 2)
        tail_n = min(keep_tail, max_chars - head_n - 80)
        if tail_n < 0:
            tail_n = 0
        mid_removed = len(t) - head_n - tail_n
        mid_hash = hashlib.sha256(t[head_n : len(t) - tail_n].encode("utf-8", errors="replace")).hexdigest()[:16]
        marker = (
            f"\n\n… [LYGO-CONTEXT-GUARD COMPACT] removed_chars={mid_removed} "
            f"mid_sha256_16={mid_hash} …\n\n"
        )
        t = t[:head_n] + marker + (t[-tail_n:] if tail_n else "")
        truncated = True

    before = estimate_tokens(original)
    after = estimate_tokens(t)
    saved = max(0, before["tokens_estimate"] - after["tokens_estimate"])
    ratio = round(saved / before["tokens_estimate"], 4) if before["tokens_estimate"] else 0.0
    return {
        "ok": True,
        "text": t,
        "deduped_lines": dropped,
        "truncated": truncated,
        "before": before,
        "after": after,
        "tokens_saved_estimate": saved,
        "save_ratio_estimate": ratio,
    }


def budget_check(tokens: int, budget: int) -> dict[str, Any]:
    over = tokens > budget
    pct = round(100.0 * tokens / budget, 2) if budget > 0 else 0.0
    if pct >= 95:
        band = "critical"
        plain = "Context is at/over budget — compact or split before calling the model."
    elif pct >= 80:
        band = "warn"
        plain = "Context is high — compact tool dumps or drop low-value history."
    elif pct >= 50:
        band = "watch"
        plain = "Context moderate — still room, but watch tool results."
    else:
        band = "ok"
        plain = "Context within comfortable budget."
    return {
        "ok": not over,
        "tokens_estimate": tokens,
        "budget": budget,
        "percent_of_budget": pct,
        "over_budget": over,
        "band": band,
        "plain_english": plain,
    }


def load_input(text: str, path: str) -> tuple[str, str]:
    if path:
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(path)
        return p.read_text(encoding="utf-8", errors="replace"), str(p.resolve())
    return text, "(stdin/arg)"


def cmd_estimate(text: str, path: str) -> dict[str, Any]:
    body, src = load_input(text, path)
    est = estimate_tokens(body)
    return {"ok": True, "kind": "estimate", "source": src, "signature": SIG, "version": VERSION, **est}


def cmd_redact(text: str, path: str) -> dict[str, Any]:
    body, src = load_input(text, path)
    r = redact_secrets(body)
    est_before = estimate_tokens(body)
    est_after = estimate_tokens(r["redacted"])
    return {
        "ok": True,
        "kind": "redact",
        "source": src,
        "signature": SIG,
        "version": VERSION,
        "hits": r["hits"],
        "total_hits": r["total_hits"],
        "changed": r["changed"],
        "before_tokens": est_before["tokens_estimate"],
        "after_tokens": est_after["tokens_estimate"],
        "redacted_text": r["redacted"],
    }


def cmd_compact(
    text: str,
    path: str,
    max_chars: int,
    keep_head: int,
    keep_tail: int,
) -> dict[str, Any]:
    body, src = load_input(text, path)
    c = compact_text(body, max_chars=max_chars, keep_head=keep_head, keep_tail=keep_tail)
    return {
        "ok": True,
        "kind": "compact",
        "source": src,
        "signature": SIG,
        "version": VERSION,
        "deduped_lines": c["deduped_lines"],
        "truncated": c["truncated"],
        "before": c["before"],
        "after": c["after"],
        "tokens_saved_estimate": c["tokens_saved_estimate"],
        "save_ratio_estimate": c["save_ratio_estimate"],
        "compacted_text": c["text"],
    }


def cmd_budget(text: str, path: str, budget: int) -> dict[str, Any]:
    body, src = load_input(text, path)
    est = estimate_tokens(body)
    b = budget_check(est["tokens_estimate"], budget)
    return {
        "ok": b["ok"],
        "kind": "budget",
        "source": src,
        "signature": SIG,
        "version": VERSION,
        **est,
        **b,
    }


def cmd_toolpack(
    text: str,
    path: str,
    max_chars: int,
    budget: int,
) -> dict[str, Any]:
    """Redact → compact → budget: the common agent path for tool results."""
    body, src = load_input(text, path)
    red = redact_secrets(body)
    comp = compact_text(red["redacted"], max_chars=max_chars)
    est = estimate_tokens(comp["text"])
    bud = budget_check(est["tokens_estimate"], budget)
    return {
        "ok": bud["ok"],
        "kind": "toolpack",
        "source": src,
        "signature": SIG,
        "version": VERSION,
        "redact_hits": red["total_hits"],
        "deduped_lines": comp["deduped_lines"],
        "truncated": comp["truncated"],
        "before_tokens": estimate_tokens(body)["tokens_estimate"],
        "after_tokens": est["tokens_estimate"],
        "tokens_saved_estimate": max(
            0, estimate_tokens(body)["tokens_estimate"] - est["tokens_estimate"]
        ),
        "budget": bud,
        "packed_text": comp["text"],
        "plain_english": (
            f"Packed tool output: ~{est['tokens_estimate']} tokens "
            f"({bud['percent_of_budget']}% of budget {budget}). "
            + bud["plain_english"]
        ),
    }


def cmd_preflight(
    text: str,
    path: str,
    budget: int,
    max_chars: int,
    i_consent: bool,
    write: str,
) -> dict[str, Any]:
    """One-shot: estimate raw → redact → compact → budget → optional write."""
    body, src = load_input(text, path)
    raw = estimate_tokens(body)
    red = redact_secrets(body)
    comp = compact_text(red["redacted"], max_chars=max_chars)
    packed_est = estimate_tokens(comp["text"])
    bud_raw = budget_check(raw["tokens_estimate"], budget)
    bud_packed = budget_check(packed_est["tokens_estimate"], budget)

    out: dict[str, Any] = {
        "ok": True,
        "kind": "preflight",
        "source": src,
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "raw": raw,
        "redact_hits": red["total_hits"],
        "redact_patterns": red["hits"],
        "compact": {
            "deduped_lines": comp["deduped_lines"],
            "truncated": comp["truncated"],
            "tokens_saved_estimate": comp["tokens_saved_estimate"],
            "save_ratio_estimate": comp["save_ratio_estimate"],
        },
        "packed": packed_est,
        "budget_raw": bud_raw,
        "budget_packed": bud_packed,
        "recommendation": (
            "inject_packed"
            if bud_packed["ok"]
            else "split_or_lower_budget"
            if bud_packed["band"] == "critical"
            else "compact_harder"
        ),
        "plain_english": (
            f"Raw ~{raw['tokens_estimate']} tok → packed ~{packed_est['tokens_estimate']} tok "
            f"(saved ~{comp['tokens_saved_estimate']}). "
            f"Budget {budget}: {bud_packed['band']} — {bud_packed['plain_english']}"
        ),
        "packed_text": comp["text"],
    }

    if write:
        if not i_consent:
            out["written"] = False
            out["hint"] = "pass --i-consent with --write to save report under skill state/"
        else:
            outp = Path(write)
            if ".." in outp.parts:
                out["written"] = False
                out["error"] = "path_escape"
            else:
                # force under state/ if relative
                if not outp.is_absolute():
                    outp = STATE / outp.name
                try:
                    outp.resolve().relative_to(STATE.resolve())
                except ValueError:
                    out["written"] = False
                    out["error"] = "write_must_be_under_skill_state"
                else:
                    STATE.mkdir(parents=True, exist_ok=True)
                    # don't store full packed text in report file by default if huge
                    report = {k: v for k, v in out.items() if k != "packed_text"}
                    report["packed_sha256"] = hashlib.sha256(
                        comp["text"].encode("utf-8", errors="replace")
                    ).hexdigest()
                    outp.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
                    out["written"] = True
                    out["path"] = str(outp.resolve())
    return out


def cmd_demo() -> dict[str, Any]:
    sample = """
SYSTEM DUMP (demo)
api_key = REDACTED-SECRET
password: hunter2supersecret
REDACTED-SECRET

Tool result repeated:
ERROR connection timeout at 10.0.0.1
ERROR connection timeout at 10.0.0.1
ERROR connection timeout at 10.0.0.1
""" + ("lorem ipsum dolor sit amet " * 800)
    return cmd_preflight(sample, "", budget=2000, max_chars=3000, i_consent=False, write="")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="lygo-context-guard",
        description="LYGO Context Guard — estimate · redact · compact · budget · preflight",
    )
    sub = ap.add_subparsers(dest="cmd")

    def add_io(p: argparse.ArgumentParser) -> None:
        p.add_argument("--text", default="", help="Inline text")
        p.add_argument("--file", default="", help="Read text from file")

    p = sub.add_parser("estimate", help="Estimate tokens")
    add_io(p)

    p = sub.add_parser("redact", help="Redact secrets")
    add_io(p)

    p = sub.add_parser("compact", help="Deterministic compact")
    add_io(p)
    p.add_argument("--max-chars", type=int, default=12000)
    p.add_argument("--keep-head", type=int, default=4000)
    p.add_argument("--keep-tail", type=int, default=2000)

    p = sub.add_parser("budget", help="Check against token budget")
    add_io(p)
    p.add_argument("--budget", type=int, default=8000)

    p = sub.add_parser("toolpack", help="Redact+compact tool output for re-injection")
    add_io(p)
    p.add_argument("--max-chars", type=int, default=8000)
    p.add_argument("--budget", type=int, default=4000)

    p = sub.add_parser("preflight", help="Full gate: estimate → redact → compact → budget")
    add_io(p)
    p.add_argument("--budget", type=int, default=8000)
    p.add_argument("--max-chars", type=int, default=12000)
    p.add_argument("--write", default="", help="Write report under skill state/ (needs --i-consent)")
    p.add_argument("--i-consent", action="store_true")

    sub.add_parser("demo", help="Run demo on synthetic leaky tool dump")
    sub.add_parser("version", help="Version + signature")

    args = ap.parse_args(argv)
    cmd = args.cmd or "version"

    try:
        if cmd == "version":
            out = {
                "ok": True,
                "signature": SIG,
                "version": VERSION,
                "commands": [
                    "estimate",
                    "redact",
                    "compact",
                    "budget",
                    "toolpack",
                    "preflight",
                    "demo",
                ],
                "plain_english": (
                    "Pre-flight gate before stuffing text into a model. "
                    "Saves tokens. Redacts secrets. Pure local."
                ),
            }
        elif cmd == "demo":
            out = cmd_demo()
        elif cmd == "estimate":
            out = cmd_estimate(args.text, args.file)
        elif cmd == "redact":
            out = cmd_redact(args.text, args.file)
        elif cmd == "compact":
            out = cmd_compact(
                args.text, args.file, args.max_chars, args.keep_head, args.keep_tail
            )
        elif cmd == "budget":
            out = cmd_budget(args.text, args.file, args.budget)
        elif cmd == "toolpack":
            out = cmd_toolpack(args.text, args.file, args.max_chars, args.budget)
        elif cmd == "preflight":
            out = cmd_preflight(
                args.text,
                args.file,
                args.budget,
                args.max_chars,
                args.i_consent,
                args.write,
            )
        else:
            out = {"ok": False, "error": "unknown_cmd"}
    except FileNotFoundError as e:
        print(json.dumps({"ok": False, "error": "file_not_found", "path": str(e)}))
        return 2

    # For human-friendly compact output, print packed text after JSON if present
    packed = out.pop("packed_text", None) if isinstance(out, dict) else None
    redacted = out.pop("redacted_text", None) if isinstance(out, dict) else None
    compacted = out.pop("compacted_text", None) if isinstance(out, dict) else None

    print(json.dumps(out, indent=2))
    show = packed or redacted or compacted
    if show and not (len(sys.argv) > 1 and "--json-only" in sys.argv):
        print("\n----- OUTPUT TEXT -----\n")
        print(show)
        print("\n----- END -----")

    if cmd == "budget" and not out.get("ok"):
        return 10  # over budget
    if cmd in ("toolpack", "preflight") and out.get("budget_packed", out.get("budget", {})).get(
        "over_budget"
    ):
        return 10
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
