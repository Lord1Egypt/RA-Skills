"""TypeSafe Jev decision head + escalation triggers. Output = enum + index only."""
from __future__ import annotations

import re

# `_jev_ask(questions, api_key=None, endpoint=None) -> list[dict]` is BOUND AT IMPORT
# from the copied helpers of perplexity-skill/src/perplexity_toolkit/console_judge.py
# (jev_ask/_post_http/_validate_choice/_api_key, MIT, browser-use/jev-ultrafast
# adaptation comment preserved). Question payload shape is taken from that file —
# never re-invented. Tests monkeypatch `policy._jev_ask`.
from ._jev_vendor import jev_ask_adapter as _jev_ask

# Post-probe sweep 2026-09-24 (docs/2026-09-24-probe-report.md): confidence is
# UNCALIBRATED (median 0.57, correct at 0.19, error at 0.42) -> tau is only a
# gross-failure gate; error control comes from structural gates + DONE verify.
TAU = 0.20
JEV_OUTAGE_N = 3
NO_TARGET_OPS = {"WAIT", "SCROLL_UP", "SCROLL_DOWN", "DONE", "BLOCKED"}
# State-level ops are never element-bound: always valid choices regardless of the table.
STATE_LEVEL_OPS = {"WAIT", "DONE", "BLOCKED"}
OPS_ORDER = ["CLICK", "TYPE_TEXT", "SELECT", "SCROLL_UP", "SCROLL_DOWN", "WAIT", "DONE", "BLOCKED"]

# Escalation reason constants (returned by needs_escalation / set on decisions).
ESC_REASONS = ("low_confidence", "done_verify", "invalid_target", "unsupported_op")


class JevUnavailable(RuntimeError): ...


def _questions(rows: list[dict], goal: str, state_sig: str) -> list[dict]:
    op_union: list[str] = []
    for r in rows:
        for o in r["ops"]:
            if o not in op_union:
                op_union.append(o)
    if not op_union:
        op_union = ["WAIT", "BLOCKED"]
    compat = [r for r in rows if r["ops"]]
    q1 = {"type": "choice", "instructions":
          f"Browser automation step. Goal: {goal}. State: {state_sig}. "
          "Pick the single best next OPERATION from the options.",
          "criteria": {o: o for o in OPS_ORDER
                       if o in op_union or o in STATE_LEVEL_OPS} or {"WAIT": "wait"}}
    q2 = {"type": "choice", "instructions":
          "Same state. Each option is '<index>' -> '<role>: <name/value>' for "
          "one element. Pick the index whose element best fits the operation.",
          "criteria": {str(r["idx"]): _row_desc(r) for r in compat} or {"-1": "none"}}
    return [q1, q2]


def _row_desc(r: dict) -> str:
    # Ops are part of the label: the target question is independent of the op
    # question in one forward, so the model must SEE what each row supports.
    desc = str(r.get("name") or r.get("value") or "").strip() or "(unnamed)"
    return f"{r.get('role', '?')}: {desc[:50]} [{','.join(r.get('ops', []))}]"


def _parse(answers: list[dict], rows: list[dict]) -> dict:
    op = str(answers[0].get("choice", "")).strip()
    tgt_raw = str(answers[1].get("choice", "")).strip()
    conf = min(float(answers[0].get("confidence", 0.0)),
               float(answers[1].get("confidence", 0.0)))
    target = None
    if op not in NO_TARGET_OPS:
        m = re.match(r"^\s*(\d+)", tgt_raw)
        target = int(m.group(1)) if m else None
    return {"op": op, "target": target, "confidence": conf, "source": "jev",
            "reason": None, "value": None}


class JevClient:
    def __init__(self, api_key: str | None = None, endpoint: str | None = None):
        self.api_key, self.endpoint = api_key, endpoint

    def decide(self, rows: list[dict], goal: str, state_sig: str) -> dict:
        try:
            answers = _jev_ask(_questions(rows, goal, state_sig),
                               api_key=self.api_key, endpoint=self.endpoint)
        except Exception as e:
            raise JevUnavailable(str(e)) from e
        return _parse(answers, rows)


def needs_escalation(decision: dict, tau: float = TAU,
                     rows: list[dict] | None = None) -> str | None:
    if decision.get("source") == "escalation":
        return None
    op = decision.get("op")
    if op not in OPS_ORDER:
        return "unsupported_op"
    if op == "DONE":
        return "done_verify"
    if rows is not None and op not in NO_TARGET_OPS:
        tgt = decision.get("target")
        row = next((r for r in rows if r["idx"] == tgt), None) if tgt is not None else None
        if row is None:
            return "invalid_target"
        if op not in row.get("ops", []):
            # e.g. TYPE_TEXT aimed at a CLICK-only link: escalate, never act
            return "invalid_target"
    if float(decision.get("confidence", 0.0)) < tau:
        return "low_confidence"
    return None


class OutageCounter:
    def __init__(self, n: int = JEV_OUTAGE_N):
        self.n, self.streak = n, 0

    def record(self, ok: bool) -> bool:
        self.streak = 0 if ok else self.streak + 1
        return self.streak >= self.n
