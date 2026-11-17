# jev-webbridge Speed Report (T10) — 2026-09-24

Real end-to-end run on Perplexity, goal = a multi-part personal finance research question (details redacted).

## Result

```json
{"status": "done", "cycles": 13, "turns": {"escalations": 7},
 "wall_ms": 1472666, "session": "jev-bc229b70ebc4"}
```

- Exit code 0. Answer extracted; DONE keyword gate passed (14/14 goal tokens present in the quoted query line + body).
- Page actually delivered: thread `perplexity.ai/search/0ce41d1f…`, full cited Chinese answer (allocation details redacted).

## Time decomposition (the honest numbers)

| Component | Value |
|---|---|
| Total wall (first receipt → final print) | 1472.7 s (24.5 min) |
| Parked waiting for the human escalation answers | **≈1299 s (88%)** — 6 gaps of 144–302 s (my own reply latency between tool calls) |
| Active machine loop (observe+Jev+act+settle, 13 cycles) | **≈29 s → ~2.2 s/cycle** |
| Sum of act durations | 13.9 s (fills 63–171 ms; clicks 5.5 s worst = bringToFront+trusted rung on first occluded click) |
| Jev decision latency | 0.60–1.0 s/cycle (698 ms avg over the 30-case final probe) |
| Projected wall with an instant escalation responder (scripted/LLM API ~1 s) | **≤45 s** |

Spec §9a target was “main-model turns ≤2 per ask”: actual = 7 escalations. Cause breakdown (receipts): `stuck`×3 (page hydration/thinking plateaus — and **interactive answer latency itself creates further stuck cycles**: parked >2 min ⇒ same state_sig ⇒ stuck again), `invalid_target`×3 (Jev pairing a target-requiring op with an incompatible row while the answer streamed; the structural gate caught all 3 — correct behavior, wasteful of turns), `done_verify`×1 (spec-mandated). Verdict: mechanically sound, **turn count fails the ≤2 acceptance — v2 must replace the interactive stdin escaler with a ~1 s API responder and record the pre-gate Jev decision in the receipt** so these are diagnosable without payload archaeology.

## Ladder evidence (occlusion handled)

- rung1 `bring_to_front+trusted_mouse_click`: succeeded once window was fronted (cycle 6, submit).
- rung2 `cdp_dispatch_mouse_event` / cdp fill: used for cycles 1, 2, 4, 5 (background-window clicks).
- rung3 synthetic: unused. rung0 (no-target ops): 6. Blocked: 0. Screenshots: taken on failure paths only (none needed for terminal status).

## Live bugs found & fixed during benching (all TDD, suite now 55 passed / ruff clean)

1. settle `time.sleep(poll_ms)` — ms fed to seconds ⇒ every mutating step slept 100 s (unit tests never traversed the path).
2. row ordinal ≠ element index (`els[idx]` vs skipped rows) ⇒ stamps on wrong elements ⇒ every targeted act failed.
3. Receipts JSONL corruption (stale append-handle offsets vs in-place `complete()` rewrite).
4. `detail` (executor error text) dropped by `record.update` — errors were opaque.
5. q2 labels hid per-row ops ⇒ Jev paired TYPE_TEXT with links.
6. No op⊆row structural gate ⇒ `invalid_target` escalations now fire instead of guaranteed fill errors.
7. TYPE_TEXT had no text source ⇒ wired caller `--text` → goal.
8. CLI had no `--url`/navigate ⇒ no tab to observe.
9. OPS marked `role=textbox` without contenteditable typeable — extension only fills native/CE (over-approx removed).

Open v2 findings (not blocking): Perplexity `fill` sets DOM text but **React/ProseMirror draft needs an input-event sync** before submit (worked around in-run by hand; belongs in the site predicate as `post_fill_js`); pre-gate Jev decisions not recorded; interactive escaler amplifies `stuck`.

## Probe gate (spec §8)

- Run 1: 30/30 · Run 2 (τ sweep): 29/30 · **Final post-fix re-run: 29/30, 698 ms/decision** (`tests/fixtures/probe_result_final.json`) — miss = id7 model variance (different id each run, never repeated). ≥26/30 ⇒ **Jev head KEEP** stands. τ = 0.20 (confidence uncalibrated).

## v2 — same-day verification run (official: run3, zero manual intervention)

```json
{"status": "done", "cycles": 13, "turns": {"escalations": 12}, "wall_ms": 76957}
```

| Metric | v1 (interactive escaler) | v2 (instant LLM escaler) | Δ |
|---|---|---|---|
| Wall | 1472.7 s (24.5 min) | **77.0 s** | **19.1×** |
| Escalation latency | 144–302 s (human, parked) | 2.8–10.1 s spans incl. loop work (flash call ~2–3 s) | ~40–80× |
| Main-model manual turns | 7 (spec ≤2 FAIL) | **0** (goal write + final read only) | meets spec intent |
| Machine act time | 13.9 s | 8.7 s | — |
| Escalations | 7 | 12 (stuck×8, invalid_target×3, done_verify×1) | more, but ~free |

Breakdown: c0/c1 transient-hydration fill errors (2, open finding), c2 submit via **synthetic_click rung 2 — first live proof of the effect-verified ladder** (CDP mouse events landed 3× in the diagnostic run and were silently ignored by the submit handler; `el.click()` fired it), c3–c11 gate/stuck escalations answered by `scripts/jevw-escaler.py` (mimo-v2.6-flash), c12 DONE → done_verify → keyword gate → done. `pre_gate` recorded on all 3 invalid_target escalations. Full answer artifact: kept local only (personal content, not shipped).

Diagnostic run disclosure: the earlier `runs_v2diag.jsonl` run received one hand-fired synthetic click mid-run (the evidence-gathering step that located the CDP silent-no-op); it is not used for the numbers above.

## Baseline comparison

- Today's manual effort for the same class of task (the Grok-6 model switch): ~30 min, multiple manual turns, **failed** (menu/occlusion).
- Prior manual research flows through this pipeline: 5–7 main-model turns, minutes per turn of model latency.
- This run, machine portion: **29 s**. With an instant responder: one command, ~45 s, 1 mechanical loop + N sub-second escalations.
