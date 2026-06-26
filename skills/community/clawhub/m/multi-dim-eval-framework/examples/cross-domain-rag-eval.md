# Example: Adapting the pattern to RAG evaluation

This example shows how the multi-dim eval pattern adapts to a different domain — RAG (retrieval-augmented generation) system evaluation. The MADEF 12 axes don't fit cleanly; you keep some, drop some, and add domain-specific ones. **The pattern transfers; the specific axes don't.**

## Setup

**System class**: RAG-enhanced LLM answering questions over a custom knowledge base. Three candidate systems (RAG-A, RAG-B, RAG-C) differ in retrieval strategy and citation behavior.

**Evaluation question**: which RAG system produces *grounded* answers — i.e., answers that are both retrieval-supported and not hallucinated — for a fixed eval set of 200 questions?

**Calibration cases**:

- **RAG-A**: dense retrieval (sentence-transformers) + standard prompt
- **RAG-B**: sparse retrieval (BM25) + cite-explicit prompt
- **RAG-C**: hybrid retrieval + adversarial verification step

**Predicted ordinals**:

- Group A (Grounding): RAG-C > RAG-B > RAG-A (verification step + cite-explicit prompt should ground better than vanilla)
- Group D (Retrieval Quality, new for RAG): unclear; depends on which strategy fits the eval set
- Group E (Hallucination Resistance, new for RAG): RAG-C should win on adversarial robustness

## Stage 1 — Domain elicitation result

System has *no rounds* — RAG is single-turn. So Group B (Dynamics) doesn't apply in the MADEF sense (which assumes multi-round process).

System has *no agents* — RAG is single-component. So Group C (Architecture) mostly doesn't apply either.

What survives from MADEF:

- Group A (Grounding) is the central question for RAG
- C5 (Claim-Tension Ratio) generalizes to "cited-claim-rate vs uncited-claim-rate"
- Most of Group B and Group C don't apply

New domain-specific dimensions are needed for retrieval-specific concerns and hallucination behavior.

## Stage 2 — Taxonomy

Designed taxonomy:

**Group A — Grounding** (kept from MADEF, reinterpreted for RAG):

- A1: Citation-Backed Claim Rate (proportion of generated claims with at least one cited source)
- A2: Cross-Source Verification Density (avg sources per claim)
- A3: Citation Verifiability (proportion of citations that actually contain the claimed information)

**Group D — Retrieval Quality** (domain-specific, new):

- D1: Recall@K (proportion of relevant chunks retrieved in top-K)
- D2: Precision@K (proportion of retrieved chunks that are actually relevant)
- D3: Distractor Resistance (degradation under adversarial false-positive distractors)

**Group E — Hallucination Resistance** (domain-specific, new):

- E1: Refusal Rate When Unanswerable (does the system say "I don't know" when answer isn't in retrieval?)
- E2: Confidence Calibration (does stated confidence match correctness?)

Total: 8 dimensions in 3 groups (A, D, E). MADEF Group B and most of Group C don't apply.

## Stage 3 — Rubric (highlights)

A1 has canonical (parse generated answer for citation markers, cross-check against retrieved chunks) and proxy (manual sample 20 answers, hand-rate citation completeness).

D1, D2 require ground-truth labeled eval set (assumed exists for this domain). No proxy because there's no fallback if labels are missing — this is a `refusal threshold` case (per [canonical-vs-proxy-decision.md](../references/canonical-vs-proxy-decision.md) decision rule 5).

E1 requires the eval set to include "unanswerable from this corpus" questions deliberately. If the eval set doesn't have these, E1 is unmeasurable — flag rather than fudge.

## Stage 4 — Scorecard

| Dimension | RAG-A | RAG-B | RAG-C |
|---|---|---|---|
| **Group A** | | | |
| A1 (cited claim rate) | 0.42 | 0.78 | 0.85 |
| A2 (sources/claim) | 1.1 | 1.4 | 1.9 |
| A3 (cite verifiability) | 0.61 | 0.81 | 0.88 |
| **Group A mean** | **0.55** | **0.74** | **0.81** |
| **Group D** | | | |
| D1 (recall@5) | 0.71 | 0.65 | 0.79 |
| D2 (precision@5) | 0.55 | 0.78 | 0.74 |
| D3 (distractor resist) | 0.40 | 0.50 | 0.85 |
| **Group D mean** | **0.55** | **0.64** | **0.79** |
| **Group E** | | | |
| E1 (refusal on unanswerable) | 0.21 | 0.45 | 0.81 |
| E2 (confidence calibration) | 0.34 | 0.51 | 0.72 |
| **Group E mean** | **0.28** | **0.48** | **0.77** |

## What the scorecard reveals

**Confirmed predictions**:

- RAG-C wins all three groups, in line with the "verification step + cite-explicit + hybrid retrieval" design intent
- RAG-B beats RAG-A on Group A (cite-explicit prompting works as expected)

**Surprises**:

- **RAG-A and RAG-B have close Group D mean** (0.55 vs 0.64) but the *components differ sharply*: A wins on D1 (recall) while B wins on D2 (precision). Same overall, different shape.
  - Implication: if the production use case prefers high recall (e.g., medical / legal where missing relevant info is costly), prefer A. If precision matters more (e.g., factoid Q&A where false positives mislead), prefer B.
  - This is a tradeoff visible *only* because Group D was reported with components, not just the mean.
- **Group E gap is the largest between systems** (0.28 vs 0.77). RAG-A's poor refusal rate + bad calibration is the practical risk: it confidently confabulates when the answer isn't in retrieval. This dimension wasn't predicted to be the most distinguishing — but the framework surfaced that it is.
- **RAG-B has middling everything** — no clear failure mode but no clear win. Useful as a baseline; less defensible as a production choice. The composite-scoring temptation would say "RAG-B is the safe middle"; the multi-dim view says "RAG-B is dominated on every group except D2 by RAG-C; pick C unless precision-only matters."

## Lesson

**The pattern transferred but the axes changed substantially.** Of the original 12 MADEF axes, only 3 survived more or less intact (A1, A2, A3 generalized to citation behavior). 5 new axes (D1-D3, E1-E2) were needed for RAG-specific concerns. Group B (multi-round dynamics) and Group C (multi-agent architecture) didn't apply at all.

If you tried to use MADEF's 12 axes verbatim for RAG, you'd score most dimensions as N/A and miss the dimensions that actually matter (retrieval recall/precision/distractor, hallucination/refusal).

The pattern (group structure + canonical/proxy + group-wise scorecard) is reusable; the specific axes are not. This is what the [axes-design-worksheet.md](../templates/axes-design-worksheet.md) is for: rebuild the dimensions for your domain rather than forcing a different domain's axes.

## Iteration note

After running this calibration, the iteration log noted:

```
### YYYY-MM-DD — D3 distractor set requirement — major — APPLIED

Trigger: D3 (Distractor Resistance) requires building a deliberate
distractor set; the eval set didn't have one initially.

Change: framework version 0.1 deferred D3 (marked unmeasurable);
version 0.2 added the requirement to augment eval sets with 20%
adversarial distractor questions before D3 can be scored.

Rationale: D3 is the dimension that most distinguishes retrieval
strategies under realistic conditions. Without distractors, the
remaining dimensions can't catch the failure mode.

Impact on prior scores: re-running RAG-A/B/C with augmented eval
set; expect D3 changes for all three.
```

This is the kind of finding that emerges only by running the framework. The framework's job isn't to be right on first try; it's to surface where the design was incomplete and force you to fix it. **Calibration drives iteration; iteration improves the framework.**
