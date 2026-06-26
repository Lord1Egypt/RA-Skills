# Example: MADEF applied to 4 multi-agent deliberation experiments

This example shows the full workflow on a real (sanitized) calibration: applying the 12-axis MADEF taxonomy to 4 multi-agent deliberation experiments. Names are anonymized to V1 / V2 / V3 / V4 (in chronological order) but the score patterns and the calibration journey are real.

## Setup

**System class**: multi-agent deliberation (3-5 agents debating a product/architecture question across 13-20 rounds)

**Calibration cases**:

- **V1**: 3 agents (Action / Guardian / Observer), 20 rounds, no claims infrastructure (legacy)
- **V2**: 4 agents (added Critic for adversarial perspective), 20 rounds, no claims infrastructure
- **V3**: 5 agents (added domain expert), 20 rounds, no claims infrastructure but has tension `source` field
- **V4**: 4 agents (Action / Guardian / Observer / Critic), 13 rounds, full claims+verifications infrastructure

**Predicted ordinals before scoring**:

- Group A (Grounding): V4 >> V1 ≈ V2 ≈ V3 (claims infra is the differentiator)
- Group B (Dynamics): V2 > V1 (Critic should push disagreement up); V3 > V2 in failure mode discovery (more agents); V4 vs V2 unclear (this is the experimental question)
- Group C (Architecture): comparable across V1-V3 (similar schema growth); V4 has C5 non-zero by construction

## Stage 1 — Data availability per case

| Case | decisions.jsonl | tensions.jsonl | claims.jsonl | round markdowns |
|---|---|---|---|---|
| V1 | ✓ | ✓ (no source field) | ✗ | ✓ |
| V2 | ✓ | ✓ (with source) | ✗ | ✓ |
| V3 | ✓ (partial — drops mid-experiment) | ✓ (with source, partial) | ✗ | ✓ |
| V4 | ✓ | ✓ | ✓ + verifications.jsonl | ✓ |

V1-V3 require fallback proxy for A1, A3 and possibly B2 (markdown sampling). V3 specifically has state integrity issues that propagate to multiple dimensions. V4 has canonical data for all 12 axes.

## Stage 2 — Taxonomy applied

The full 12-axis MADEF taxonomy applies (it was designed for this domain). 3 groups:

- Group A — Grounding: A1, A2, A3
- Group B — Dynamics: B1, B2, B3, B4
- Group C — Architecture: C1, C2, C3, C4, C5

No domain-specific additions. (Other domains might add: e.g., for tool-using agents, "tool call success rate" / "tool selection precision" might be group D.)

## Stage 3 — Rubric (highlights)

For V1-V3, A1 falls back to proxy (count decisions explicitly referencing prior tension/decision IDs). V3 attaches `⚠ state incomplete` flag because state files dropped mid-experiment.

For V4, A1 uses canonical (claims status proportion). C5 is meaningful only for V4; V1-V3 score 0 by construction.

For C1, all four cases attach `C1_note` because all have an adversarial agent (V1 has Guardian functioning adversarially; V2-V4 have explicit Critic).

## Stage 4 — Scorecard summary

| Dimension | V1 | V2 | V3 | V4 |
|---|---|---|---|---|
| **Group A** | | | | |
| A1 | 0.50 ⚠ proxy | 0.66 ⚠ proxy | 0.42 ⚠ proxy + state incomplete | 0.91 |
| A2 (normalized / raw) | 1.00 / 2.0 | 1.00 / 3.0 | 1.00 / 4.0 | 1.37 / 4.1 |
| A3 | 0.42 ⚠ proxy | 0.55 ⚠ proxy | 0.30 ⚠ proxy + state incomplete | 0.78 |
| **Group A mean** | **0.64** | **0.74** | **0.57** | **0.85** |
| **Group B** | | | | |
| B1 (slope) | +0.12 | +0.18 | +0.05 | +0.21 |
| B2 (rate/round) | 1.8 | 2.1 | 2.9 | 2.2 |
| B3 (with 5a/5b) | 5 (5a×1) | 5 (5a×1) | 10 (5a×1, 5b×1) | 5 (5a×1) |
| B4 | 1.0 (3/3 pass) | 1.0 | 0.83 (5/6 pass) | 1.0 |
| **Group B mean** | **0.54** | **0.61** | **0.71** | **0.59** |
| **Group C** | | | | |
| C1 | 0.92 | 0.93 (C1_note: critic 6%) | 0.89 | 0.85 (C1_note: critic 6%) |
| C2 | 4.0/5 | 4.5/5 | 4.5/5 | 4.7/5 (full 4-role stress grid) |
| C3 | 0.05 (manual coding) | 0.18 | 0.25 | 0.22 |
| C4 | 0.77 | 0.74 | 0.71 | 0.37 (claims/verif inflates schema count) |
| C5 | 0 | 0 | 0 | 0.90 |
| **Group C mean** | **0.55** | **0.55** | **0.55** | **0.66** |

## What the scorecard reveals

**Confirmed predictions**:

- V4 is highest on Group A (Grounding) by a wide margin — claims infra works as intended
- V2 > V1 on Group B (added Critic raises disagreement and discovery)
- C5 is non-zero only for V4 (structural by construction)

**Surprises**:

- **V3 outscores V4 on Group B mean** (0.71 vs 0.59). Why? V3's higher B2 (failure mode discovery) and unique 5b finding (cross-agent dependency at 5 agents) drive its B group up. V4 is shorter (13 rounds vs 20) so has fewer total opportunities for B3 progress. **The Group B story is more nuanced than "V4 wins everything."**
- **Group A V3 < V1** despite V3 having more agents and Critic (0.57 vs 0.64). Audit: V3's narrative compression ("All Agents (compressed)" paragraphs) collapses 4 perspectives into one, mechanically lower per-agent grounding density. **More agents without expanding round structure compresses per-agent depth.** This is a finding the framework surfaced; it would have been invisible under composite scoring.
- **C4 collapses for V4** (0.37) because claims/verifications infrastructure shows up in schema node count. The rubric should distinguish *product schema* from *evaluation infrastructure*. → iteration_log entry added.

## Iteration log entry from this calibration

```
### YYYY-MM-DD — C4 product/eval-infra distinction — minor — APPLIED

Trigger: V4 scoring. Schema node count includes claims+verifications
infrastructure, dropping C4 to 0.37 vs ~0.75 for V1-V3.

Change: madef-axes.md C4 section now explicitly excludes evaluation
infrastructure from schema node count. C4 measures *product* growth,
not *measurement* growth.

Rationale: claims/verif is overhead for *evaluation*, not for the
deliberation product. Including it conflates two things.

Impact on prior scores: V4 C4 re-scored at 0.74 after exclusion.
```

## Lesson

**The Group B surprise (V3 outscoring V4 on dynamics) is what the framework is for.** A single-composite score would have shown "V4 highest" and stopped there. The group-wise scorecard reveals that V4's claims-infra advantage is in Group A; in Group B, V3's longer rounds and 5-agent population produced more discovery and a unique system-layer finding.

If the user's evaluation question is "did claims infra improve grounding?", the answer is yes (Group A). If the question is "did claims infra improve everything?", the answer is more interesting — and only the multi-dim scorecard makes that interesting answer visible.

The C4 iteration also shows the framework working as designed: an unexpected result (V4 collapsing on Architectural Economy) prompted a rubric clarification, not a "V4 has worse architecture" claim. Calibration drives iteration; iteration improves the framework. Without the calibration, the C4 issue would have shipped silently.
