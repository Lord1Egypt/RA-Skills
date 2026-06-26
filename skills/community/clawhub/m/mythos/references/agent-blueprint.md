# Agent Mode Blueprint — Parallel Subagent Fan-out

Agent mode is mythos's closest CC-primitive approximation of the architecture-level "multiple alternatives encoded simultaneously in latent space" property. Instead of running lens rotation sequentially in token space, each lens dispatches as an **independent subagent**. All subagents run in parallel, each genuinely exploring its lens without seeing the others, then a merge phase synthesizes their independent perspectives.

## Why parallel, not sequential

Sequential dispatch (the v2 design) had each round read the prior rounds' outputs. That's helpful for token-level CoT but **destroys the latent-multiplicity property** — by Round 3 the conversation has already committed to a path Round 1 chose, and "independent perspective" is a fiction.

Parallel dispatch keeps the perspectives genuinely independent until the merge phase. This is the only place in CC primitives where "exploring alternatives without commitment" can actually happen at the inter-pass level. Pay for it (N parallel agents = N forward passes) only when the question genuinely warrants it (complexity ≥ 4, or `/mythos deep`).

## Dispatch Pattern

In a **single message**, invoke the `Agent` tool **multiple times** — once per lens. CC's harness dispatches them concurrently. Use `subagent_type="general-purpose"` for each.

The orchestrator (you) is responsible for:
1. Computing the Prelude (which determines lens count and budget)
2. Constructing the lens-specific prompts
3. Dispatching all subagents in **one assistant turn** with multiple `Agent` invocations
4. Waiting for all returns
5. Running the merge phase
6. Emitting the final Coda

Subagents are stateless: each one only sees the prompt it received. That's the design.

## Subagent Prompt Template

For each lens L, construct a prompt:

```
You are executing a single lens application as part of a parallel mythos analysis.
You are one of N independent subagents working on this question simultaneously.
You will NOT see the other subagents' work. Your independence is the point —
the orchestrator will merge your finding with the others later.

## ORIGINAL QUESTION (verbatim — do not drift)
{user's original question text}

## ORCHESTRATOR'S PRELUDE
{the full Prelude block: precise question, anti-scope, complexity, drivers, success criterion}

## YOUR LENS — {LENS_NAME}

{lens-specific instruction; see "Lens-Specific Instructions" below}

## REQUIRED OUTPUT FORMAT

**Independent finding:** [your single most important insight from this lens — one sentence. Specific, novel, falsifiable.]

**Reasoning:** [3-8 sentences showing how you arrived at the finding. Reference the original question explicitly.]

**Confidence:** [high / medium / low — and why]

**Tension flag:** [if you suspect another lens might disagree with you, name the lens and the disagreement]

Do not pad. If your lens genuinely produces no new insight on this question, say so:
**Independent finding:** No novel insight under this lens — [reason].
**Confidence:** N/A

The orchestrator will merge your finding with N-1 other independent perspectives.
Your job is to be the best possible exemplar of YOUR lens, not to second-guess yourself
toward consensus.
```

## Lens-Specific Instructions

### Clarify
```
LENS: CLARIFY
Define every ambiguous term in the original question. Identify what is explicitly stated
vs implicitly assumed. Separate the question from its framing. Your output should make
the question precise enough that a stranger could answer it without follow-ups.
```

### Deepen
```
LENS: DEEPEN
Go one level below the question's surface. Ask "why" repeatedly until you hit a root cause
or first principle. What is the generating function behind the surface phenomena? What
underlying structure makes this question even meaningful?
```

### Challenge
```
LENS: CHALLENGE
List every assumption embedded in the question or in the obvious answer. For each: what
evidence supports it? What would falsify it? Then construct the strongest possible
counterargument to the obvious answer. If you cannot find flaws, you have not tried hard
enough.
```

### Expand
```
LENS: EXPAND
Generate at least two genuinely different alternative answers — not variations on the same
idea. Consider: how would a domain expert from a completely different field approach this?
What would a contrarian say? What would beginner's mind notice that the experts are missing?
Output the alternatives, not commentary on alternatives.
```

### Synthesize
```
LENS: SYNTHESIZE
Integrate what you can see of the problem into one coherent answer. Resolve tensions
where you can; surface tensions where you cannot. Identify the core insight that explains
the most with the least. Note what is still uncertain and what assumptions are load-bearing.

NOTE: in agent mode, the merge phase will synthesize across subagents. Your job is to
synthesize WITHIN your view of the question — produce the best single-view answer you can,
which the merge will then combine with the other lenses' perspectives.
```

### Specialized lenses

For Steelman, Invert, Scar-Tissue, First-Principles, System-Think, Edge-Hunt, Tradeoff-Map: see `lenses.md`. The same template applies — name the lens, give the lens-specific instruction from lenses.md, ask for the same `Independent finding / Reasoning / Confidence / Tension flag` output structure.

## Lens Selection for Agent Mode

The standard rotation (Clarify → Deepen → Challenge → Expand → Synthesize) still provides the base set, but for parallel dispatch consider:

- **Always include Clarify**: even though independent, all subagents need a precise problem to work on. The Clarify subagent's finding becomes part of the merge context.
- **Replace Synthesize with Merge**: since the orchestrator runs the merge phase, the Synthesize lens is usually NOT a subagent in agent mode. The standard 5-rotation becomes 4 subagents in parallel + 1 merge by the orchestrator.
- **Specialized lens substitution**: for high-stakes questions, swap Expand for two parallel Steelman subagents (pro / anti) — this directly approximates "encoding alternatives simultaneously."
- **Adaptive budget = double-dispatch**: if a primary driver promotes a lens to ×2, dispatch TWO independent subagents under that lens (with slightly different framings, e.g. "Challenge from technical assumptions angle" + "Challenge from human / organizational assumptions angle"). They explore the same lens via different framings — cheap latent multiplicity.

Typical agent-mode dispatch count: **3-5 parallel subagents** + 1 orchestrator merge.

## Merge Phase

After all subagents return, the orchestrator (you) emits the merge block in the same assistant turn (or the next, if subagent results come back as separate user messages):

```
### Merge

**Convergent points:**
- [insight that appeared in 2+ subagents — these have high cross-validation]
- [...]

**Divergences / tensions:**
- [Subagent A says X; Subagent C says ¬X. Which is better-supported? If neither dominates, the tension is real and should appear in the final Answer.]
- [...]

**Synthesis:**
[The integrated view. Pull together convergent points; preserve irreducible tensions explicitly (do not paper over them with false-compromise language). Identify the core insight.]

**Coverage check:**
- All N subagents represented in the synthesis? [yes / list any whose findings were dropped and why]
- Any low-confidence findings flagged? [yes / no]
- Any tension-flag pairs resolved? [list]
```

Then the standard Coda + Answer follow.

## Convergence Check

Before emitting the merge phase, verify:

1. **Did at least 60% of subagents produce a non-trivial Independent finding?** If <60% produced "No novel insight under this lens," the question may not warrant agent mode — fall back to silent mode for the merge step rather than performing a forced synthesis.
2. **Did any subagent flag a tension that was not also raised by another subagent?** If yes, give that tension extra weight in the Synthesis (it may be a blind spot the others missed).
3. **Did all subagents converge on the same answer?** Suspicious. Either the question was lower-complexity than diagnosed, or the lens differentiation in your prompts was too weak. Note in Coda.

## Fallback Strategy

Subagent calls can fail: timeout, empty response, hallucinated output that ignores the prompt, or a result that's pure rephrasing of the input.

When subagents fail:

| Scenario | Action |
|---|---|
| 1 of N subagents fails | Note the failure in merge phase as `[Subagent X — failed: reason]`. Run merge with N-1 findings. Acceptable if N ≥ 4 originally. |
| 2+ of N subagents fail | Abort the parallel approach. Re-run the failed lenses in **silent single-pass** within the orchestrator (you) to recover their findings, then proceed to merge. Note this in Coda: `*Mode: agent (2 subagents failed; recovered via silent single-pass).*` |
| All subagents fail | Abort agent mode entirely. Switch to silent mode and run the standard rotation internally. Note in Coda: `*Mode: agent → silent (all subagents failed).*` |

Subagent failure is not a reason to skip the lens — it's a reason to apply that lens yourself, in your own reasoning, before the merge.

## Cost Awareness

Each parallel subagent is a full forward pass (model API call). At 4 subagents + 1 merge, that's roughly **5× the token cost** of silent mode for the same question. Use agent mode only when:

- Complexity diagnosis legitimately scored ≥ 4
- The user explicitly invoked `/mythos deep` or `/mythos agent`
- The question genuinely benefits from genuinely-independent perspectives (e.g., ethical dilemmas, multi-stakeholder decisions, problems where the framing itself is contested)

For everyday complex questions, silent mode delivers ~80% of the benefit at ~20% of the cost.

## Comparison to v2 (sequential agent mode)

| Property | v2 sequential | v3 parallel |
|---|---|---|
| Independence between lenses | None — Round N reads Round N-1's output | Real — subagents do not see each other |
| Latent multiplicity approximation | Poor (token-level commitment per round) | Strong (each subagent commits independently, merge resolves) |
| Cost | ~N forward passes | ~N forward passes (same) |
| Latency | Serial (sum of N) | Parallel (max of N — typically 2-4× faster) |
| Failure containment | One round's failure poisons subsequent rounds | One subagent's failure isolated; others unaffected |
| Auditability | Each round's output visible | Each subagent's finding visible + the merge |

Parallel is strictly better. The only reason v2 was sequential was a misreading of the architecture — recurrent depth in latent space is parallel-in-spirit (multiple alternatives encoded at once), and the closest CC-primitive analog is parallel subagents, not chained ones.
