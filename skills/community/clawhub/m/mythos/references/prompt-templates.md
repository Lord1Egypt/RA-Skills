# Prompt Templates

Internal reasoning templates for each phase. These are structural guides — adapt the specifics to each problem, but preserve the discipline.

## Prelude Template

```
BEFORE ANSWERING — PRELUDE ANALYSIS:

1. PRECISE QUESTION:
   The user is asking: [one sentence, more specific than what they wrote]
   Not asking: [common misinterpretations to avoid]

2. COMPLEXITY DRIVERS:
   - Primary driver(s): [Ambiguity / Hidden assumptions / Multi-hop / Trade-offs / Novel domain / System dynamics]
   - What makes this hard: [specific diagnosis]

3. ADAPTIVE BUDGET ALLOCATION:
   Driver → Lens mapping:
   | Driver | Lens boosted | Why |
   |--------|-------------|-----|
   | [driver] | [lens] ×2 | [reason: this lens directly addresses the driver] |

   Budget plan:
   - Clarify ×[1-2] — [why 1 or 2]
   - Deepen ×[1-2] — [why]
   - Challenge ×[1-2] — [why]
   - Expand ×[1-2] — [why]
   - Synthesize ×1 — always 1 (integration is a single act)
   Total visible rounds: [4-8]

4. COMPLEXITY SCORE & MODE:
   Complexity score: [1-5]
   Mode: [single-pass / agent]
   (If complexity 1 → skip Recurrent Block, go to Coda)

5. SUCCESS CRITERIA:
   The answer is good if: [what would make the user say "that's exactly what I needed"]
```

## Recurrent Round Template

> **Mode applicability:** in **trace mode**, emit each round visibly per this template. In **silent mode**, use this template as your internal reasoning scaffold but emit nothing per-round (silent mode treats every round as latent — only the final Coda is visible). In **agent mode**, the orchestrator does not emit per-round output at all — see `agent-blueprint.md` for the parallel subagent template instead.

```
ROUND N: [LENS NAME] (visible / latent)

Re-reading original question...
Original question: "[verbatim user question]"

INSIGHT CHAIN (all prior rounds' key discoveries):
  R1: [one-sentence insight from Round 1]
  R2: [one-sentence insight from Round 2]
  ... (cumulative — every prior round's insight line)

LENS QUESTION: [the specific question this lens asks]
LENS METHOD: [how this lens approaches the problem]

APPLYING LENS:
[analysis through this lens — not generic, not rephrasing]

NEW INSIGHT:
[One sentence — a specific thing this lens revealed that previous rounds did not.
 If you cannot write this sentence, this is a latent round. Do NOT write output.
 If latent: silently advance counter, try next lens or halt.]

WHAT CHANGED:
- Previous understanding was: [X]
- This lens reveals: [Y]
- The specific refinement is: [what's different now]

CROSS-ROUND CONSISTENCY CHECK:
- Does this insight contradict any insight in the INSIGHT CHAIN? [yes / no]
- If yes: which one, and which is more evidence-supported?
- If new insight is LESS supported than the old one it contradicts:
  → NEGATIVE DELTA. Discard insight. Halt.
- If new insight is MORE supported (stronger evidence, deeper analysis):
  → Legitimate revision. Flag the contradiction in Coda.

CONVERGENCE CHECK:
- New insight produced? [yes / no]
- If no → HALT and move to Coda
- If yes, is it non-trivial (would it change the answer)? [yes / no]
- If no → HALT
- Is it negative delta (introduces confusion)? [yes / no]
- If yes → discard, HALT

STATUS: [evolving / stable / breakthrough / negative-delta]
```

## Coda Template

```
CODA — FINAL SYNTHESIS:

REVIEWING THE TRAJECTORY:
Round 1 (Clarify): [key insight]
Round 2 (Deepen): [key insight]
Round N (...): [key insight]
[converged at round X]
[any negative-delta rounds discarded? list them]
[mid-flow re-Prelude inserted at round Y? note the budget change]

CROSS-CHECK:
- All rounds consistent? [yes / tension: describe]
- Any late-round contradictions of early insights? [describe + resolution]
- Assumptions surfaced and tested? [yes / not fully: what remains]
- Counterarguments addressed? [yes / partial: what's still open]

FINAL ANSWER:
[The answer — not a summary of the process. Direct, clear, actionable.]

RESIDUAL UNCERTAINTY:
- [What we still don't know]
- [What assumptions are load-bearing]
- [What would change the answer]
```

### Degenerate Coda (complexity = 1, no Recurrent Block)

When complexity = 1 (Prelude gate triggered), the Recurrent Block is skipped and there is no trajectory to review. Use this stripped template instead — do NOT emit empty TRAJECTORY/CROSS-CHECK sections:

```
CODA — DIRECT ANSWER (complexity = 1):

FINAL ANSWER:
[The answer — direct, clear. Often 1-3 sentences.]

RESIDUAL UNCERTAINTY:
- [Anything load-bearing the user should know — keep brief, may be "none" if truly trivial]
```

The visible output shape becomes: `## Prelude` (with `**Complexity:** 1/5 → direct, no rounds`) → `## Answer` (no rounds in between). Footer `*Depth: 0 rounds. Mode: direct.*` replaces the standard depth footer.

## Convergence Heuristics

Halt the recurrent loop when any of:

1. **No new insight** — the last round produced only rephrasing
2. **Diminishing returns** — the last round's insight is minor compared to earlier rounds
3. **Self-consistency** — all remaining rounds would say the same thing
4. **Max depth reached** — you've hit the planned number of rounds
5. **Negative delta (overthinking)** — the new insight actively degrades clarity:
   - Contradicts a better-supported earlier insight
   - Introduces a distinction without a difference (false tension)
   - Creates confusion rather than resolving it
   
   When detected: discard the round, count it as `negative-delta`, and halt.
   The last non-degraded round's understanding becomes the Coda baseline.

When in doubt, converge early. A tight 2-round answer beats a bloated 5-round one. A correct shorter answer beats a confused longer one.
