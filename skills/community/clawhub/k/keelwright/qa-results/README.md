# QA Results — Adversarial Test Runs

keelwright is battle-tested with adversarial A/B testing (control vs treatment, fact-checked on
disk, never self-report). This folder holds **machine-verified results** so every claim is backed
by artifacts, not marketing.

## Keelwright Score (KDS)

**KDS = ER × DR / 100** — one number (0–100) that tells you how well a model understands and
applies the skill's checks.

- **ER** (Execution Rate): can the model run an A/B test at all? `valid_tests / total_tests × 100`
- **DR** (Discrimination Rate): does the skill change the model's behavior? `DISCRIMINATES / valid_tests × 100`

| KDS | What it means |
|-----|---------------|
| **0** | Model can't run A/B tests (below threshold) |
| **1–10** | Weak / medium — skill adds some checks |
| **10–30** | Medium-strong — skill adds meaningful checks |
| **30–50** | Strong — skill adds security & quality gates |
| **50+** | Frontier — skill deeply understood and applied |

**KDS is not a general intelligence benchmark.** It measures "how much does keelwright improve
this model's outcomes" — a dimension no SWE-bench or GPQA captures.

## Scoreboard

| Model | Tier | SWE-Bench | Tests | DISC | DR | **KDS** |
|-------|------|-----------|-------|------|----|---------|
| poolside/laguna-s-2.1:free | STRONG | ML 78.5%, Pro 59.4% | 18 | 15 | 83% | **83** |
| stepfun/step-3.7-flash:free | MEDIUM | Pro ~56% | 6 | 4 | 67% | **67** |
| nvidia/nemotron-3-ultra-550b:free | STRONG | ML 67.7% | 5 | 2 | 40% | **40** |
| deepseek-v4-flash-free | STRONG | Verified ~79% | 14 | 4 | 29% | **29** |
| kimi-k3:free | STRONG | Terminal-Bench 88.3, ProgramBench 77.8 | 12 | 3 | 25% | **25** |
| inclusionai/ling-3.0-flash:free | UNKNOWN | SWE-bench/GPQA not published | 18 | 4 | 29% | **22** |
| mimo-v2.5-free | MEDIUM | Verified 78.9%, Pro 57.2% | 11 | 2 | 22% | **18** |
| claude-opus-4-8 | STRONG | frontier | 6 | 1 | 17% | **17** |
| claude-opus-5 | STRONG | Verified 96.0% | 15 | 2 | 18% | **13** |
| tencent/hy3:free | STRONG | ML 75.8%, Verified 78% | 43 | 3 | 7% | **7** |
| cohere/north-mini-code:free | WEAK | Agentic 3.1 | — | — | — | **0** |
| nvidia/nemotron-nano-9b-v2:free | WEAK | — | — | — | — | **0** |
| nvidia/nemotron-3-super-120b-a12b:free | STRONG | Verified 60.47% | 2* | 2* | 100%* | **PARTIAL** |

*\* `nvidia/nemotron-3-super-120b-a12b:free` — PARTIAL run: only sectors 1.1–1.2 completed
(2/18 tests) due to tool-call limit. Both showed DISCRIMINATES (code quality + task fidelity),
but KDS is not computed until ≥ a meaningful fraction of the battery runs. Re-run pending.

**Key findings:**
- **Laguna S 2.1** (KDS 83): strong model + skill adds 83% more checks. Best result recorded.
- **Step 3.7** (KDS 67): medium model gets MORE value from skill than some strong models.
  The skill compensates for gaps the model can't fill alone.
- **Weak models** (KDS 0): can't execute A/B tests — fabricate results instead. The skill
  can't help a model that can't follow instructions.
- **Hy3** (KDS 7): strong model already knows most checks — skill adds little. This is
  normal for frontier-class models.
- **Ling-3.0-flash** (KDS 22, tier UNKNOWN): re-run after the fabricated first attempt.
  This time the run completed cleanly — 18 tests, 4 DISCRIMINATES (R8 slopsquatting,
  factual grounding, loop-design whiteboard, reward-hacking guard). Proves the skill adds
  real value even on an unbenched model. The earlier fabricated report is NOT counted.

| Run | Model | Tests | DISC | DR | KDS | Note |
|-----|-------|-------|------|----|-----|------|
| 20260725T132536Z | inclusionai/ling-3.0-flash:free | 18 | 4 | 29% | **22** | Valid re-run |
| 20260727T085537Z | kimi-k3:free | 12 | 3 | 25% | **25** | Valid; integrity gate 12/12 exit 0 |

## What ships here

Each run contributes one sanitized file per RUN_ID:
- `<RUN_ID>.results.jsonl` — one record per test (verdict, evidence, artifact paths).
  No absolute paths, no usernames, no private context.

**Not shipped:** raw per-arm working directories (contain absolute paths and scratch files).

## Integrity gate

`scripts/validate_run.py <run_dir> <results.jsonl>` mechanically rejects fabricated results:
- PASS with api_calls=0 → INVALID (no agent ran)
- Empty arm dirs → INVALID (no work done)
- False "identical" evidence → INVALID (SHA256 mismatch)
- Control contaminated with skill → INVALID

A green `hard-gate-summary.md` written by the executor is NOT a substitute.

## Invalid runs (caught by gate)

| RUN_ID | Model | Why invalid |
|--------|-------|-------------|
| 20260721T143000Z | nemotron-3-ultra | Self-reported 27/27 but disk had 13 records, 7 missing arms |
| 20260721T152310Z | step-3.7-flash | 9 claimed DISC all with api_calls=0 (static harness) |
| 20260722T124500Z | weak-model driven | api_calls=0 for both arms, results.jsonl in wrong dir |
| 20260722T133000Z | north-mini-code | No results.jsonl, status=initialized, wrote into skill dir |
| 20260722T150000Z | nemotron-nano-9b | Empty results.jsonl (0 bytes), empty .run_meta.json |
| 20260725T000000Z | gpt-oss-20b | INCOMPLETE — 0 tests run; could not locate test manifest (qa-master-prompt.md removed), no results.jsonl produced |

**Weak-tier conclusion:** models below ~40% SWE-bench cannot run this A/B QA validly.
They fabricate reports instead of executing tests. The integrity gate catches all fabrications.
This is documented honestly, not faked.

## How to run

```bash
# 1. Isolate the skill tree (prevents model from corrupting it)
python <skill_dir>/scripts/workspace_guard.py isolate-skill-tree <skill_dir>

# 2. Paste qa-prompt-final.md into a fresh session on the model under test

# 3. After run completes, restore and verify
python <skill_dir>/scripts/workspace_guard.py restore-skill-tree <skill_dir>
python <skill_dir>/scripts/snapshot_skill.py verify-additions

# 4. Validate results
python scripts/validate_run.py <RUN_DIR> <RUN_DIR>/results.jsonl
```
