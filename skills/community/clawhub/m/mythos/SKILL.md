---
name: mythos
description: Recurrent-depth reasoning via iterative refinement. Use for complex analysis, multi-hop problems, design decisions, strategic planning — any question where single-pass answers would be shallow.
version: 0.1.1
title: Mythos Skill
author: chitinlabs
type: command
category: research
invocation: /mythos
tags: [reasoning, recurrent-depth, multi-round, latent-reasoning, claude-code]
homepage: https://github.com/chitinlabs/mythos-skill
license: MIT
---

# Mythos — Recurrent-Depth Reasoning

Implements a prompt-layer protocol inspired by the Recurrent-Depth Transformer pattern (OpenMythos hypothesis). The protocol is **three modes**, each mapping to a different CC primitive that approximates a different facet of latent-space recurrence:

- **Silent** (default): Recurrent Block runs in your internal/extended-thinking reasoning. The user sees only the Coda — a compact Answer plus a one-line trajectory hint. Closest to the architectural mythos property of *no token-level commitment between loops*.
- **Trace** (opt-in via `trace` keyword): Recurrent Block runs as visible token-level rounds with explicit insight chain. Maximally auditable. Use for teaching, debugging, deep-analysis posts where reviewers must verify each step.
- **Agent** (default for complexity ≥ 4, opt-in via `deep`/`agent` keyword): Lenses dispatched as **parallel subagents** that explore independently, then a merge phase synthesizes them. Closest to the latent-multiplicity property of mythos — multiple alternatives explored truly in parallel before commitment.

Invoke via `/mythos <question>` or the Skill tool. Mode keywords:
- `/mythos trace …` → force trace mode (visible rounds)
- `/mythos deep …` or `/mythos agent …` → force agent mode (parallel fan-out)
- `/mythos quick …` → force silent mode (override agent default at high complexity)

## The Pattern

```
[User Question]
     ↓
[PRELUDE]        — decompose, score complexity, pick mode + lens sequence
     ↓
[RECURRENT × N]  — iterative refinement, three flavors:
   silent: lens rotation runs internally; no per-round emission
   trace:  lens rotation emits visible rounds with insight chain
   agent:  lenses dispatched as N parallel subagents, then merged
     ↓
[CODA]           — cross-check, surface residual uncertainty, deliver
```

**Why three modes?** Architecture-level mythos (per OpenMythos hypothesis) reasons in continuous latent space — multiple reasoning paths encoded simultaneously, no token output between loops. The closest CC primitives to that property are:
- **Internal/extended-thinking reasoning** for "no per-step token commitment" → **silent mode**
- **Parallel independent forward passes** for "multiple alternatives explored simultaneously" → **agent mode**
- Visible token rotation trades that faithfulness for auditability → **trace mode**

Silent is the default because it preserves the latent-exploration property cheapest. Trace is opt-in because it has real value (debugging, teaching) but only when explicitly wanted.

## Mode Selection

After Prelude:
- complexity = 1 → **direct** (skip Recurrent Block; use degenerate Coda)
- complexity 2-3 → **silent mode**
- complexity 4-5 → **agent mode**

Complexity score (1 point each): multi-hop dependencies, ambiguous trade-offs, likely hidden assumptions, novel domain, high-stakes decision.

### Mode keywords (parsed from invocation args / user message)

Keywords are case-insensitive. Take only a **leading bare word** in slash-command args (e.g. `/mythos trace …` strips `trace` from the question). If multiple keywords appear in the wider user message, **last-wins**. Keywords apply AFTER complexity is computed — they override routing, not diagnosis.

| Keyword         | Effect                                                       |
|-----------------|--------------------------------------------------------------|
| `trace`         | Force trace mode (visible rotation) regardless of complexity |
| `deep`, `agent` | Force agent mode (parallel fan-out) even at complexity ≤ 3   |
| `quick`         | Force silent mode even at complexity ≥ 4                     |

Examples:
- `/mythos How do I structure my CSS?` → silent (complexity ~2)
- `/mythos trace Should we adopt Conventional Commits?` → trace mode for the same question
- `/mythos deep Should we rewrite the renderer?` → agent fan-out (parallel subagents)
- `/mythos quick Pivot or stay?` → silent even though Pivot question would normally route to agent

### Mid-flow mode escalation (one per session)

The Prelude diagnosis can be wrong — Round 2 sometimes reveals a primary driver that was invisible at the start. When this happens:

1. Insert a **re-Prelude** block with the same template as STEP 1, plus `(re-Prelude after Round N)` in the heading
2. Update budget allocation only — do NOT discard prior rounds' insights (the insight chain or thinking-state carries forward)
3. If the re-scored complexity crosses the agent-mode threshold, escalate from silent/trace to agent for remaining lenses; document the escalation in Coda
4. **Silent → Trace escalation**: if Round 2 in silent mode surfaces a controversy the user needs to verify, you may switch to trace mode for the remaining rounds. Note this in Coda.
5. Limit: **one re-Prelude per session**. Repeated re-Preludes signal scope drift, not improving accuracy — halt and use what you have.

Re-Prelude only when the *diagnosis* was wrong (a driver was missed). Do NOT re-Prelude just because a round produced a surprising insight under a known driver — that's normal recurrent depth.

## Output Modes

### Silent mode (default)

The Recurrent Block runs **internally** — apply the Prelude's lens sequence in your own reasoning (use `<thinking>` extended-thinking blocks if available, otherwise apply the rotation as ordinary internal pre-output reasoning). Each lens must genuinely change your view of the problem; latent rounds (lens applied internally with no new insight) silently advance. Apply convergence criteria internally; if a new line of reasoning contradicts a well-supported earlier insight (negative delta), discard.

The user sees ONLY the Coda:

```
## Answer
[direct, complete, actionable answer — typically 1-5 paragraphs]

---
*Depth: N latent passes. Mode: silent. Lens path: Clarify → Deepen → Challenge → Synthesize.*
*Load-bearing assumptions: [what would change the answer if wrong]*
```

For complexity = 1 (direct path), the footer collapses to:
```
*Depth: 0 rounds. Mode: direct.*
```

### Trace mode (opt-in via `trace` keyword)

Full visible rotation, the historically-original mythos behavior. The user sees:

```
## Prelude
**Q:** [precise restatement] | **Not:** [anti-scope]
**Complexity:** [score]/5 → trace mode (forced), [total rounds] total | **Drivers:** [...]
**Budget:** Clarify ×[n] → ...
**Success:** [...]

### Round 1: Clarify
**New insight:** [one sentence]
**What changed:** [...]
**Convergence:** evolving / stable / breakthrough / negative-delta

### Round 2: Deepen
**Insight chain:** [R1: ...]
**New insight:** [...]
...

## Answer
[...]

---
*Depth: N rounds, converged at round X. Mode: trace.*
*Load-bearing assumptions: [...]*
```

Cross-round attention is explicit via the **insight chain**: from Round 2 onward, each round shows a 3-5 line summary of every prior round's "New insight" line, so later rounds cannot forget earlier discoveries.

### Agent mode (default for complexity ≥ 4, opt-in via `deep`/`agent`)

Each lens dispatches as an **independent subagent in parallel** (single message, multiple `Agent` tool invocations). After all return, a **merge phase** synthesizes the independent perspectives. This approximates the architecture-level "multiple alternatives encoded simultaneously" property — each subagent really explores its lens without seeing the others.

```
## Prelude
[full diagnostic, like trace mode]

[Dispatching 4 parallel subagents: Clarify, Deepen, Challenge, Steelman]

### Subagent A — Clarify
**Independent finding:** [...]
**Confidence:** high/medium/low

### Subagent B — Deepen
**Independent finding:** [...]
**Confidence:** ...

### Subagent C — Challenge
**Independent finding:** [...]
**Confidence:** ...

### Subagent D — Steelman
**Independent finding:** [...]
**Confidence:** ...

### Merge
**Convergent points:** [insights present across multiple subagents]
**Tensions:** [places where subagents genuinely disagree]
**Synthesis:** [the integrated view, with tensions preserved if irreducible]

## Answer
[...]

---
*Depth: N parallel subagents merged. Mode: agent.*
*Load-bearing assumptions: [...]*
```

Read `references/agent-blueprint.md` for the parallel dispatch pattern, lens-specific subagent prompts, and fallback strategy when subagents fail.

## Process

### STEP 1: Prelude — Understand, Diagnose, Allocate

Read `references/prompt-templates.md` for the full Prelude template.

1. Restate the core question — more precise than the user's phrasing
2. Anti-scope — what is explicitly NOT being asked
3. Complexity score (1-5) → mode selection
4. **Complexity diagnosis** — identify the *primary complexity drivers* (pick 1-3):
   - Ambiguity: key terms are vague or undefined
   - Hidden assumptions: the question likely rests on unexamined premises
   - Multi-hop: the answer requires chaining multiple reasoning steps
   - Trade-offs: the core difficulty is weighing competing values
   - Novel domain: the problem space is unfamiliar or unprecedented
   - System dynamics: the problem is embedded in a complex system with feedback loops
5. **Adaptive budget allocation** — assign round budgets per lens based on drivers (read `references/lenses.md` for the full driver→lens mapping):

   | Primary Driver | Lenses that get 2 rounds (or 2 subagents in agent mode) |
   |---------------|---------------------------------------------------------|
   | Ambiguity | Clarify |
   | Hidden assumptions | Challenge, Steelman |
   | Multi-hop | Deepen, System-Think |
   | Trade-offs | Tradeoff-Map, Expand |
   | Novel domain | First-Principles, Expand |
   | System dynamics | System-Think, Edge-Hunt |

   Total rounds: typically 4-8 (silent/trace), 3-5 parallel subagents (agent).

6. Lens sequence — use the standard rotation as base sequence, with per-lens budget
7. Success criterion — what makes the answer good enough to stop

**Gate:** If complexity = 1, skip the Recurrent Block entirely. Go directly to STEP 3 (Coda) and use its **degenerate path** (no trajectory review — see prompt-templates.md).

### STEP 2: Recurrent Block — Iterative Deep Refinement

**Standard rotation (lens sequence, applies to all modes):**

| Round | Lens | Question |
|-------|------|----------|
| 1 | Clarify | Define terms. Remove ambiguity. What's the precise question? |
| 2 | Deepen | Root causes, first principles, generating functions — one level deeper |
| 3 | Challenge | What assumptions? What's the strongest counterargument? |
| 4 | Expand | What alternatives? What would a different expert see? |
| 5 | Synthesize | Integrate all perspectives into one coherent answer |

For specialized lenses (System-Think, Edge-Hunt, Tradeoff-Map, Invert, Scar-Tissue, First-Principles, Steelman), read `references/lenses.md`.

**Adaptive budget:** A lens may get 2 consecutive applications (2 rounds in silent/trace, 2 parallel subagents in agent) if it addresses a primary complexity driver. For the 2nd application, find a new angle, stress-test the 1st conclusion, or go one level deeper. If the 1st application already converged (status = stable), skip the 2nd.

**Mode-specific execution:**

- **Silent mode**: Re-read the original question before each lens application (the `e` injection). Apply the lens in your internal reasoning. The lens must change how you see the problem — not just relabel it. Run latent rounds freely (apply lens internally with no emission). Halt per convergence criteria below. The Recurrent Block produces no visible output; only the Coda is emitted.

- **Trace mode**: Re-read the original question before each round. Each round emits the per-round template:
  ```
  ### Round N: [Lens]
  **Insight chain:** [R1: ... → R2: ...]   (only when 2+ prior rounds exist)
  **New insight:** [one sentence]
  **What changed:** [...]
  **Convergence:** evolving / stable / breakthrough / negative-delta
  ```
  Hard constraint: if you cannot produce a concrete new insight in a single sentence, the round has failed. Rephrasing under a new label is failure → halt.

- **Agent mode**: See `references/agent-blueprint.md`. Dispatch parallel subagents in a single message (multiple `Agent` tool invocations). Each subagent receives: original question (verbatim) + Prelude + lens-specific instruction. Subagents do NOT see each other's intermediate work — that's the point. After all return, run the merge phase as described in the blueprint.

**Convergence — halt when ANY of:**

1. **No delta** — round/lens output is substantively identical to a prior round
2. **Trivial delta** — new insight is minor compared to earlier insights
3. **Self-consistent** — answer is coherent, assumptions surfaced, counterarguments addressed
4. **Max rounds reached** — total visible rounds (or parallel subagents in agent mode) hit the Prelude budget
5. **Negative delta (overthinking)** — the new insight actively degrades quality:
   - Contradicts a well-supported earlier insight without strong new evidence
   - Introduces confusion (distinction without a difference, false tension)
   - Hallucinated under the current lens
   
   In silent mode: discard internally and halt. In trace mode: mark the round `negative-delta`, do NOT emit the bad insight as content, halt. In agent mode: surface the divergent subagent's finding with low-confidence flag and let merge resolve it.

Anti-pattern: halting because you're tired of thinking. Check: is there an unresolved tension or unexamined assumption? If yes, one more round. But also: am I generating confusion just to fill the budget? If yes, negative delta — halt.

### STEP 3: Coda — Synthesize & Deliver

Read `references/prompt-templates.md` for the Coda cross-check template (and the **degenerate Coda** for complexity-1).

1. Review trajectory — arc from Round 1 to convergence (silent: enumerate the lens path; trace: list each round's key insight; agent: list each subagent's finding plus the merge result)
2. Cross-check — is the answer consistent with every step of the recurrent block?
3. Residual uncertainty — what's unknown, what assumptions are load-bearing
4. Deliver the answer in the mode-specific output format above

## Principles

- **The question is sacred.** Re-read it before every lens application. The question text is `e` — the original signal injected to prevent drift.
- **Each round earns its keep.** One specific new insight per round. Rephrasing = failure → halt.
- **Disagree with yourself.** Round 3 should find flaws in Round 2. That's the design, not a bug.
- **Depth over breadth.** One insight fully explored beats three shallow observations.
- **Converge and ship.** A tight 2-round answer that converged is better than a 5-round display of stamina.
- **Mode matches stakes.** Silent is fast and faithful for ordinary depth. Trace pays a token cost for auditability. Agent pays a token + latency cost for genuinely independent multi-perspective exploration. Don't default-up.
- **Insight chain (or thinking state, or parallel divergence) is your memory.** Don't let later steps forget what earlier steps discovered.
- **Mind the overthinking trap.** More rounds are not always better. If a new lens only produces confusion, that's negative delta — stop. A shorter right answer beats a longer confused one.
- **Faithfulness is a means, not an end.** The protocol exists to produce better reasoning, not to perform fidelity to a paper. If the reasoning is right, mode purity doesn't matter.

## Calibration

Run `/mythos <question>` (or `/mythos trace <question>`, `/mythos deep <question>`) on any of these to verify reasoning quality. Each case is designed to stress specific mechanisms in specific modes.

| Question | Expected silent | Expected trace | Expected agent | Mechanisms tested |
|----------|----------------|----------------|----------------|-------------------|
| "Should I use SQLite or PostgreSQL for a single-user desktop app?" | Concise answer; ≤3 lens path; no agent escalation | 2-3 visible rounds; Challenge questions framing | N/A (complexity too low — but `/mythos deep` should still produce ≥3 parallel subagents) | Complexity gate, early convergence |
| "Our startup has 3 months of runway and our product has good reviews but declining retention. Pivot or stay?" | 4-5 lens path, mentions ≥2 alternatives in Answer | 4-5 rounds; Expand round must contain ≥2 distinct alternatives; Scar-Tissue surfaces failure patterns | Parallel: Clarify + Tradeoff-Map + Scar-Tissue + Invert + Synthesize subagents; merge surfaces tension between "pivot" and "stay" | Adaptive budget, parallel divergence |
| "Design a caching strategy for a read-heavy API serving 10M users" | Answer mentions ≥1 non-obvious edge case | 3-4 rounds; Edge-Hunt round identifies stampede / herd / serialization | Parallel includes an Edge-Hunt subagent that surfaces edge cases independently | Specialized lens, overthinking detection |
| "What would make our code review process 10x more effective?" | Answer challenges the "more reviews" framing | 3-4 rounds; Challenge surfaces framing assumption visible in final Synthesize | Parallel Challenge subagent reframes the question | Cross-attention / cross-divergence |
| "Is it ethical to train AI on public web data without consent?" | Answer preserves genuine tensions, no false compromise | 4-6 rounds; Steelman builds strongest case for BOTH sides | Parallel includes 2 Steelman subagents (pro / anti) + Tradeoff-Map; merge MUST preserve irreducible tension, not paper over it | Multi-hop + hidden assumptions, false-compromise detection |

**What to watch for:**
- **Silent mode emits visible rounds:** mode routing is broken — re-read SKILL.md
- **Trace mode skips Challenge/Expand:** standard rotation is not being followed
- **Agent mode dispatches sequentially:** read `agent-blueprint.md` — parallel dispatch is the whole point
- **Synthesize / Merge ignores early findings:** cross-step memory is broken (insight chain in trace, divergence list in agent, latent state in silent)

### Automated calibration runner

From the source repo, run `install/calibrate.ps1` (PowerShell) or `bash install/calibrate.sh` (bash) to walk through all five cases interactively across all three modes. The runner prompts you for observed lens path, round/subagent count, and convergence behavior, performs structural checks against the expected baselines, and writes a timestamped report (`calibration-report-YYYYMMDD-HHMM.md`) to the same `install/` directory. The calibration runner ships only in this source repository, not in the marketplace skill bundle.

The runner is **manual by design** — quality of mythos reasoning cannot be programmatically verified, only structural properties (lens presence, round count, parallel-vs-sequential dispatch). Treat FAIL counts as signals to re-read SKILL.md, not as ground truth.
