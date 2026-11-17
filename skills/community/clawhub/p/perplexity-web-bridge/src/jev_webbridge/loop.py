"""Generic decision loop: observe -> decide -> act -> verify -> settle-wait (spec §4).

Control flow follows the plan's LOCKED list 1-7:
1. observe (ONE evaluate, OBSERVE_JS) -> rows, state.
2. decision = client.decide(...); JevUnavailable feeds the OutageCounter (streak >= 3
   forces escalation, reason "jev_outage"); needs_escalation gates (low_confidence /
   invalid_target / unsupported_op) and the stuck gate (identical consecutive
   state_sig, reason "stuck") -> escalate_fn(payload).
3. receipt is APPENDED AND FLUSHED (JSONL) BEFORE executor.act.
4. act.result == "stale" -> re-observe next cycle (counts as a cycle, no escalation).
5. mutating act (result ok, rung > 0) -> bounded settle-wait via the site predicate.
6. op DONE -> executor.extract() then independent verification: escalate once carrying
   the extract payload (reason "done_verify"), keyword check (>= half of the goal's
   casefolded content words present) -> status done / else escalate once more and
   re-extract; still failing -> fall through to the cycle cap, never fake success.
7. cycle cap -> exhausted; act.result "blocked" twice consecutively -> blocked
   (the FIRST blocked receipt escalates in-cycle, spec §7).

Receipt record fields (exactly): ts, cycle, op, target, source, reason, confidence,
state_sig, result, rung, duration_ms, escalated.

Test seams (plan-mandated, documented):
- ``answer_probe``: when set (plan tests), it supplies the extracted answer text;
  production passes None and the loop calls ``executor.extract()``.
- ``stuck_escalates``: gates the stuck trigger. The plan's verbatim test
  ``test_receipt_written_before_act`` raises on ANY escalation, so the default is
  False; production/CLI entry points should pass True (spec §4.3 stuck trigger).

A failed observe (after one whole-step retry, spec §7) degrades that cycle: rows=[]
and state_sig is prefixed "observe-error|"; no decision is taken on a failed observe
(5 consecutive failures abort with receipts).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from datetime import UTC, datetime
from typing import Any

from .executor import Executor
from .policy import TAU, JevUnavailable, OutageCounter, needs_escalation
from .predicates import get_predicate
from .table import observe, observe_js

DEFAULT_RECEIPT_PATH = "~/.jev-webbridge/runs.jsonl"
MAX_CYCLES = 20
MAX_OBSERVE_FAILURES = 5
HISTORY_TAIL = 4


def state_sig(state: dict, extras: dict | None = None) -> str:
    """Stable string serialization of observe state + predicate extras (url|text_len|title-hash)."""
    title = str(state.get("title") or "")
    title_hash = hashlib.sha256(title.encode("utf-8")).hexdigest()[:8]
    parts = [str(state.get("url") or ""), str(int(state.get("text_len") or 0)), title_hash]
    ex = extras or {}
    for key in sorted(ex):
        parts.append(f"{key}={ex[key]}")
    return "|".join(parts)


def keywords_present(goal: str, answer: str | None) -> bool:
    """DONE verification: >= half of the goal's content words (casefolded) appear in the answer."""
    words = re.findall(r"\w+", goal.casefold())
    if not words or not answer:
        return False
    low = answer.casefold()
    hits = sum(1 for w in words if w in low)
    return hits * 2 >= len(words)


class Receipts:
    """JSONL receipt sink: one line per decision, appended and flushed BEFORE act.

    ``complete`` fills result/rung/duration_ms back into that same line after act, so
    the file stays one line per decision; a crash between the two leaves the pre-act
    line with null results — the audit guarantee is the pre-act flush, not the update.
    """

    def __init__(self, path: str) -> None:
        self.path = os.path.expanduser(path)
        parent = os.path.dirname(self.path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        self.records: list[dict] = []
        self._fh = open(self.path, "ab")  # noqa: SIM115 — held open for the run; closed by run()

    @staticmethod
    def _line(record: dict) -> bytes:
        return (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")

    def write_pre_act(self, record: dict) -> int:
        """Append one receipt line and flush it immediately; returns the line's byte offset."""
        # os.path.getsize, NOT self._fh.tell(): complete() rewrites the file through a
        # second handle, which leaves the append handle's position stale -> seeks land
        # mid-line and corrupt the JSONL (live bug 2026-09-24).
        offset = os.path.getsize(self.path)
        self._fh.write(self._line(record))
        self._fh.flush()
        self.records.append(record)
        return offset

    def complete(self, offset: int, record: dict) -> None:
        """Fill the act result into the pre-act line (same line — never a second record)."""
        with open(self.path, "r+b") as fh:
            fh.seek(offset)
            fh.write(self._line(record))
            fh.truncate()

    def close(self) -> None:
        self._fh.close()


def _record(cycle: int, decision: dict, sig: str, escalated: bool,
            pre_gate: dict | None = None) -> dict:
    return {
        "ts": datetime.now(UTC).isoformat(),
        "cycle": cycle,
        "op": decision.get("op"),
        "target": decision.get("target"),
        "source": decision.get("source"),
        "reason": decision.get("reason"),
        "confidence": decision.get("confidence"),
        "state_sig": sig,
        "result": None,
        "rung": None,
        "duration_ms": None,
        "detail": None,  # executor error text (fill failed / MISMATCH / rung names)
        "pre_gate": dict(pre_gate) if pre_gate else None,  # rejected Jev decision
        "escalated": escalated,
    }


def _payload(
    reason: str, goal: str, rows: list[dict], sig: str, history: list[dict],
    answer: str | None = None,
) -> dict:
    payload = {
        "reason": reason,
        "rows": rows,
        "state_sig": sig,
        "goal": goal,
        "history": list(history[-HISTORY_TAIL:]),
    }
    if answer is not None:
        payload["answer"] = answer
    return payload


def _escalate(
    escalate_fn: Any, reason: str, goal: str, rows: list[dict], sig: str,
    history: list[dict], answer: str | None = None,
) -> dict:
    decision = dict(escalate_fn(_payload(reason, goal, rows, sig, history, answer)))
    decision["source"] = "escalation"  # spec §4.4: recorded with source escalation
    if not decision.get("reason"):
        decision["reason"] = reason
    return decision


def _observe(driver: Any) -> tuple[list[dict], dict, Exception | None]:
    """ONE OBSERVE_JS evaluate with one whole-step retry (spec §7 probe-failed).

    Returns (rows, state, error); on failure rows=[] and state is a stable empty dict.
    """
    last_error: Exception | None = None
    for _ in range(2):
        try:
            rows, state = observe(driver.evaluate(observe_js()))
            return rows, state, None
        except Exception as e:  # noqa: BLE001 — a broken observe degrades the cycle, never raises
            last_error = e
    return [], {"url": "", "text_len": 0, "title": ""}, last_error


def _decide(
    client: Any, rows: list[dict], goal: str, sig: str, tau: float, outage: OutageCounter,
) -> tuple[dict | None, str | None]:
    """-> (decision, gate_reason). gate_reason set means the caller must escalate."""
    try:
        decision = client.decide(rows, goal, sig)
    except JevUnavailable:
        if outage.record(False):
            return None, "jev_outage"
        # Below the outage threshold: safe no-op hold so the next cycle can retry.
        return (
            {"op": "WAIT", "target": None, "confidence": tau, "source": "jev",
             "reason": None, "value": None},
            None,
        )
    outage.record(True)
    if decision.get("source") == "escalation":
        return decision, None
    if decision.get("op") == "DONE":
        # done_verify is NOT escalated here: DONE verification (step 6) escalates
        # post-act carrying the executor.extract() payload.
        return decision, None
    return decision, needs_escalation(decision, tau=tau, rows=rows)


def _extract(executor: Executor, answer_probe: str | None) -> str:
    """Extract seam: answer_probe (plan tests) supplies the text; production calls extract()."""
    if answer_probe is not None:
        return str(answer_probe)
    return executor.extract()


def _verify_done(
    executor: Executor, escalate_fn: Any, goal: str, rows: list[dict], sig: str,
    history: list[dict], answer_probe: str | None, escalations: int,
) -> tuple[str | None, int]:
    """DONE verification (step 6). Returns (answer, escalations); answer None = not verified."""
    answer = _extract(executor, answer_probe)
    escalations += 1
    escalate_fn(_payload("done_verify", goal, rows, sig, history, answer))
    if keywords_present(goal, answer):
        return answer, escalations
    escalations += 1
    escalate_fn(_payload("done_verify", goal, rows, sig, history, answer))
    answer = _extract(executor, answer_probe)
    if keywords_present(goal, answer):
        return answer, escalations
    return None, escalations  # never fake success -> cap/blocked decides the status


def _probe(driver: Any, probe_js: str) -> dict | None:
    try:
        raw = driver.evaluate(probe_js)
    except Exception:  # noqa: BLE001 — probe failure just runs the wait out to its cap
        return None
    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def _settle_wait(driver: Any, predicate: dict, baseline_len: int, extras: dict) -> None:
    """Bounded useful-state wait (spec §6): poll probe_js every poll_ms collecting
    samples [(text_len, elapsed_ms)] newest-first until predicate.settled() or cap_ms.
    Never sleeps past cap_ms."""
    cap_ms = int(predicate["cap_ms"])
    poll_ms = int(predicate["poll_ms"])
    t0 = time.monotonic()
    samples: list[tuple[int, int]] = []
    while True:
        elapsed = int((time.monotonic() - t0) * 1000)
        probe = _probe(driver, predicate["probe_js"])
        if probe is not None:
            samples.insert(0, (int(probe.get("text_len") or 0), elapsed))
            extra = probe.get("extra")
            if isinstance(extra, dict):
                extras.update(extra)
            # quiet_ms arg = the probe's own DOM-quiescence duration (predicate's signal).
            if predicate["settled"](baseline_len, samples, int(probe.get("quiet_ms") or 0)):
                return
        if elapsed >= cap_ms:
            return
        # poll_ms is milliseconds; time.sleep takes SECONDS (the 100s hang).
        time.sleep(poll_ms / 1000)


def run(
    driver: Any,
    goal: str,
    site: str,
    client: Any,
    escalate_fn: Any,
    max_cycles: int = MAX_CYCLES,
    receipt_path: str = DEFAULT_RECEIPT_PATH,
    tau: float = TAU,
    answer_probe: str | None = None,
    text: str | None = None,
    max_wall_s: float = 900.0,
    wait_free: bool = False,  # CLI v2: WAIT cycles don't consume max_cycles
    stuck_escalates: bool = False,
) -> dict:
    """Run the loop to a terminal status.

    Returns exactly {"status", "answer", "turns": {"escalations"}, "cycles", "wall_ms",
    "site_checks"} with status in {"done", "exhausted", "blocked"}; wall_ms measured
    from the first observe. ``escalate_fn(payload) -> Decision`` is supplied by the CLI.
    """
    predicate = get_predicate(site)
    executor = Executor(driver)
    receipts = Receipts(receipt_path)
    outage = OutageCounter()
    extras: dict[str, Any] = {}
    escalations = 0
    blocked_streak = 0
    observe_streak = 0
    prev_sig: str | None = None
    status = "exhausted"
    answer: str | None = None
    cycles = 0
    effective = 0  # non-WAIT cycles; waiting on an external process is free
    t0 = time.monotonic()
    try:
        cycle = -1
        # Runaway guard is wall-clock: WAIT-only loops stay alive through long
        # answer generation but cannot outlive max_wall_s.
        while effective < max_cycles and (time.monotonic() - t0) < max_wall_s:
            cycle += 1
            rows, state, obs_err = _observe(driver)
            cycles = cycle + 1
            sig = state_sig(state, extras)
            if obs_err is not None:
                sig = f"observe-error|{sig}"

            # (2) stuck trigger: identical consecutive state signatures.
            gate_reason: str | None = None
            decision: dict | None = None
            if stuck_escalates and prev_sig is not None and sig == prev_sig:
                gate_reason = "stuck"
            if obs_err is not None:
                if gate_reason is None:
                    observe_streak += 1
                    prev_sig = sig
                    if observe_streak >= MAX_OBSERVE_FAILURES:
                        break  # spec §7: abort with receipts
                    effective += 1  # counts as a cycle; no decision on a failed observe
                    continue
            else:
                observe_streak = 0

            pre_gate = None
            if gate_reason is None:
                decision, gate_reason = _decide(client, rows, goal, sig, tau, outage)
            if gate_reason is not None:
                if decision is not None and decision.get("source") == "jev":
                    # v2: keep the Jev decision the gate REJECTED in the receipt —
                    # otherwise diagnosing invalid_target/low_confidence requires
                    # reconstructing the escalation payload by hand.
                    pre_gate = {"op": decision.get("op"),
                                "target": decision.get("target"),
                                "confidence": decision.get("confidence"),
                                "reason": gate_reason}
                escalations += 1
                decision = _escalate(
                    escalate_fn, gate_reason, goal, rows, sig, receipts.records
                )
            if decision is None:  # unreachable: every gate_reason path yields a decision
                raise RuntimeError(f"no decision for cycle {cycle} (gate={gate_reason})")

            # TYPE_TEXT text source (spec G3): caller-supplied text, else the goal.
            # Policy never invents text and never fabricates a value.
            if decision.get("op") == "TYPE_TEXT" and not decision.get("value"):
                decision["value"] = text if text is not None else goal
            if decision.get("op") != "WAIT" or not wait_free:
                effective += 1

            # (3) receipt WRITTEN (pre-act, flushed) -> executor.act.
            # First blocked receipt escalates in-cycle; twice in a row -> blocked.
            while True:
                record = _record(
                    cycle, decision, sig, escalated=decision.get("source") == "escalation",
                    pre_gate=pre_gate,
                )
                offset = receipts.write_pre_act(record)
                act = executor.act(decision, rows,
                                    post_fill_js=predicate.get("post_fill_js"))
                record.update(
                    result=act.get("result"),
                    rung=act.get("rung"),
                    duration_ms=act.get("duration_ms"),
                    detail=act.get("detail"),
                )
                receipts.complete(offset, record)
                if act.get("result") != "blocked":
                    blocked_streak = 0
                    break
                blocked_streak += 1
                if blocked_streak >= 2:
                    status = "blocked"
                    break
                escalations += 1
                decision = _escalate(
                    escalate_fn, "blocked", goal, rows, sig, receipts.records
                )
            if status == "blocked":
                prev_sig = sig
                break

            # (4) stale -> re-observe next cycle (counts as a cycle, no escalation).
            if act.get("result") == "stale":
                prev_sig = sig
                continue

            # (6) DONE -> independent verification with extract payload.
            if decision.get("op") == "DONE":
                answer, escalations = _verify_done(
                    executor, escalate_fn, goal, rows, sig, receipts.records,
                    answer_probe, escalations,
                )
                prev_sig = sig
                if answer is not None:
                    status = "done"
                    break
                continue  # still failing -> cap/blocked, never fake success

            # (5) mutating act -> bounded settle-wait with the site predicate.
            if act.get("result") == "ok" and act.get("rung") not in (0, None):
                _settle_wait(driver, predicate, int(state.get("text_len") or 0), extras)
            prev_sig = sig
    finally:
        receipts.close()

    return {
        "status": status,
        "answer": answer,
        "turns": {"escalations": escalations},
        "cycles": cycles,
        "wall_ms": int((time.monotonic() - t0) * 1000),
        "site_checks": summarize_checks(
            executor.post_extract_probe(predicate.get("post_extract_js"))
        ),
    }


def summarize_checks(raw: dict) -> dict:
    """Pure QA summary of a site post-extract probe (v1.1 anti-pit guards).

    - ``model_label``: provenance line if the site shows one (catches silent
      model downgrades when compared against the requested model).
    - ``citation_coverage`` / ``decorative_citations``: how many citation
      markers the body actually uses vs how many sources it lists; fewer than
      half of >=5 listed sources cited = decorative padding.
    """
    if not raw:
        return {}
    out: dict = {"model_label": raw.get("model_label")}
    listed = int(raw.get("sources_listed") or 0)
    used = int(raw.get("markers_used") or 0)
    if listed:
        out["citation_coverage"] = round(used / listed, 3)
        out["decorative_citations"] = bool(listed >= 5 and used < listed * 0.5)
    return {k: v for k, v in out.items() if v is not None}
