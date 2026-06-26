---
name: multi-dim-eval-framework
description: Designs a multi-dimensional evaluation framework for AI systems where single-score benchmarks lose information. Use when comparing experiments/agents across qualitatively different dimensions, when canonical metrics aren't available for legacy systems, or when explaining *which* dimension drove an outcome matters more than ranking.
version: 0.1.0
---

# Multi-Dimensional Evaluation Framework Designer

A skill for designing custom multi-dimensional evaluation frameworks for AI systems. Walks the user from "I have a system to evaluate" to "I have a calibrated, group-organized scorecard with canonical/proxy duality and explicit failure modes."

The central premise: **a single composite score destroys the information you need to debug** *which* dimension actually drove the outcome. This skill produces frameworks that force the reader to look at multiple numbers, with rules for when each measurement is reliable.

## Four-stage flow

- **Stage 1 — Domain elicitation**: what system, what evaluation question, what calibration cases
- **Stage 2 — Taxonomy design**: group structure + dimensions per group
- **Stage 3 — Rubric**: canonical/proxy split per dimension + failure modes
- **Stage 4 — Judgment**: group-wise scorecard interpretation (no composite)

After Stage 4, ask: *"Want to score additional cases or adjust the rubric?"* — this is the calibration loop.

## When to use

Activate when the user:

- Wants to evaluate AI systems (agents, deliberations, RAG, multi-step reasoning) across multiple qualitatively-different dimensions
- Needs to compare instances with asymmetric data availability (some have canonical metrics, others have only narrative logs)
- Has noticed single-score benchmarks miss important variation between systems
- Says "tradeoffs" — and wants to make those tradeoffs explicit per dimension
- Wants a reusable scorecard format that survives infrastructure migrations

Don't activate when:

- The user wants a single comparable benchmark number — point them at HumanEval / MMLU / domain-specific benchmarks instead
- The system has a clear single quality metric (perplexity, accuracy on a labeled set)
- The user is asking how to design *one* metric, not a *framework* of metrics

## Stage 1 — Domain elicitation

Goal: extract enough about the user's evaluation domain to design groups and dimensions.

**Turn 1 — concrete instances, not abstract criteria.** Ask:

> "Give me 1-2 concrete instances of systems you want to evaluate (or have already evaluated). What's the question that comparison should answer? — e.g., 'is system V2 more grounded than V1?' / 'does adding a Critic agent reduce sycophancy?'"

This grounds the design in real comparisons rather than generic axes.

**Turn 2 — calibration cases.** Ask:

> "Of the systems you've already run, which 2-3 do you have *strong intuitions* about — i.e., 'I expect X to score higher than Y because Z'? Those are your calibration cases."

If the user has no calibration cases yet, the framework can't be calibrated. Either:

- Run on at least 2 prior instances first, or
- Design the framework theoretically and acknowledge it's uncalibrated until run

**Turn 3 — data availability.** Ask:

> "For each calibration case, what data do you have? — structured records (jsonl, database)? narrative logs (markdown, reports)? both? Same schema across cases or different?"

This determines canonical/proxy split for Stage 3.

**Turn 4 — capability layers (optional).** If the system is complex, ask:

> "If you had to split the evaluation into 3 layers, what would they be? Examples: evidence-quality / process-dynamics / structural-form. Or: retrieval-quality / ranking-quality / adaptation-quality."

The user's natural splits become the groups. If the user can't articulate layers, default to a 3-group structure: (1) evidence/grounding, (2) process/dynamics, (3) structural/architecture. Or use the 4-family alternative shown in [memory-bench-taxonomy.md](references/memory-bench-taxonomy.md).

By end of Stage 1 you should know:

- The system class being evaluated (multi-agent / single-LLM / RAG / tool-using / etc.)
- 2-3 calibration cases with expected ordinals
- Data availability map (which cases have canonical data, which need proxy)
- Group structure (typically 3 groups, may be 2 or 4)

## Stage 2 — Taxonomy design

Author the group structure + dimensions per group.

**Step 1: Surface the [12-axis MADEF reference](references/madef-axes.md)** to the user. Ask which axes feel relevant.

Don't force the user to use all 12 — most domains use 5-8 of the MADEF axes plus 0-3 domain-specific additions. The MADEF table at the bottom of `madef-axes.md` shows likely keep/modify/drop patterns for common domains (single-LLM reasoning, tool-using agents, RAG, multi-step coding).

**Step 2: Show the [memory-bench-designer's 4-family taxonomy](references/memory-bench-taxonomy.md)** as alternative shape.

This makes the point that group structure is domain-driven. memory-bench has 4 groups (capability families) because memory has those layers. Deliberation has 3 groups (evidence/process/structure) because deliberation has those layers. Don't blindly copy — let the user's domain shape it.

**Step 3: Walk the design worksheet.** Use [axes-design-worksheet.md](templates/axes-design-worksheet.md) to fill in:

- Group names + what each layer asks
- 2-5 dimensions per group
- For each dimension: name + 1-line definition

Cap at 8-12 total dimensions. More than 12 is unmanageable; less than 4 isn't multi-dim.

## Stage 3 — Rubric

For each dimension designed in Stage 2, fill in the operational rubric using [canonical-vs-proxy-decision.md](references/canonical-vs-proxy-decision.md):

- Canonical measure (formula given full data)
- Fallback proxy (operationalization for partial data)
- Tie-break rule (partial credit cases)
- Flag conditions (when to attach `⚠`)
- Refusal threshold (when proxy is too noisy to score)

A dimension without all five fields is not yet operational — it's a sketch.

**Apply [group-design-principles.md](references/group-design-principles.md) M1-M5 meta-principles**:

- M1: ambiguous → report range, not point
- M2: population-count normalization required for cross-instance
- M3: stress conditions evaluated separately
- M4: framework must be falsifiable
- M5: calibration before claims

## Stage 4 — Judgment

Apply the framework to the calibration cases the user named in Stage 1.

For each case, populate [scorecard.md.tmpl](templates/scorecard.md.tmpl) with group-wise scores.

**Critical: report group means separately, never a composite.** A failing system with one group at 0.9 and another at 0.2 is not the same as a system with all groups at 0.55.

**Verify ordinal predictions**: do the calibration cases score in the predicted order? If not:

- Iterate the rubric and log the change in `iteration_log.md` (see [group-design-principles.md M5](references/group-design-principles.md))
- Or accept that the prediction was wrong and document why

The framework freezes (becomes versioned) when the calibration ordinals hold and at least 2-3 real adjustments have been logged.

## Quick example

User: *"I have 4 multi-agent debate experiments. The 4th one added claims+verifications infra. I want to evaluate which experiment is doing the most rigorous deliberation."*

Stage 1 reveals:

- System class: multi-agent deliberation, 3-5 agents per experiment, 13-20 rounds each
- Calibration cases: V1/V2/V3 (legacy) and V4 (with claims infra)
- Data availability: legacy has narrative round logs only; V4 has full state jsonl
- Predicted ordinals: V2 > V1 (added Critic), V3 > V2 (more agents), V4 highest on grounding (has claims infra)

Stage 2 lands on the 12-axis MADEF taxonomy in [madef-axes.md](references/madef-axes.md), with 3 groups (Grounding / Dynamics / Architecture).

Stage 3 fills in canonical/proxy for each axis. Most legacy experiments need proxy on A1, A3, B1, B2; V4 has canonical on all.

Stage 4 produces 4 scorecards. The ordinals confirm V4 is highest on Group A (Grounding) but the picture is more nuanced on Group B (V3 outscores V4 on dynamics due to more agents and a unique cross-agent finding). The framework surfaces *which* dimensions move with the architecture change, which is what the user needed.

Full walkthrough: [examples/deliberation-system-eval.md](examples/deliberation-system-eval.md).

## How the skill behaves at each turn

- **Don't** dump all 12 axes at once. Surface them in groups, ask about relevance group-by-group.
- **Don't** start with the rubric (Stage 3) before the taxonomy is settled (Stage 2). Operational definitions before the design intent is wasted work.
- **Do** push back if the user wants a single composite. The pattern's whole point is to refuse that. Explain *why* (it hides which dimension failed) rather than just refusing.
- **Do** verify calibration ordinals before the user "trusts" the framework. If the framework can't reproduce the ordinals the user predicted, *something* is wrong (rubric, prediction, or scoring) — find which.

## References

- [references/group-design-principles.md](references/group-design-principles.md) — five design principles + five meta-principles, domain-agnostic
- [references/canonical-vs-proxy-decision.md](references/canonical-vs-proxy-decision.md) — decision tree for two-track measurement
- [references/madef-axes.md](references/madef-axes.md) — 12-axis instantiation for multi-agent deliberation (use as reference, adapt to your domain)
- [references/memory-bench-taxonomy.md](references/memory-bench-taxonomy.md) — 4-family/8-dimension instantiation for memory eval (alternative shape)

## Templates

- [templates/axes-design-worksheet.md](templates/axes-design-worksheet.md) — fill-in worksheet for designing your own axes
- [templates/scorecard.md.tmpl](templates/scorecard.md.tmpl) — output format for group-wise scorecards

## Examples

- [examples/deliberation-system-eval.md](examples/deliberation-system-eval.md) — applying MADEF to 4 deliberation experiments
- [examples/cross-domain-rag-eval.md](examples/cross-domain-rag-eval.md) — adapting the pattern to RAG evaluation

## What this skill does NOT do

- It does not run benchmarks for you — it designs the framework you'll run
- It does not produce automated scoring — scoring is procedurally specified but human-in-the-loop for proxy work
- It does not collapse multi-dim into a single ranking number (refusal is the design)
- It does not validate that the dimensions you choose are *the right* dimensions for your domain — that's a calibration question, the framework only enforces self-consistency

## License

MIT
