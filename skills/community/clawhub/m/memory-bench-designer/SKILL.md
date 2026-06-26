---
name: memory-bench-designer
description: Designs a custom agent-memory benchmark for the user's specific use case. Activate when the user asks which memory strategy fits their agent, how to evaluate agent memory, or how to benchmark context/retrieval choices. Conducts elicitation, generates scenario configs, runs benchmarks across five memory strategies, and interprets results.
---

# Memory Bench Designer

An agent memory benchmark designer. The user describes their use case in natural language; you conduct a short multi-turn elicitation, write a scenario config, run the benchmark, and deliver a case-specific interpretation.

The central premise: **no single memory strategy wins across use cases**. Different scenarios reward different strategies (see references/adapter-profiles.md for empirical evidence). Your job is to figure out which scenario the user actually has, then run the benchmark that exposes which strategy fits.

## Four-stage flow

Stage 1 **Understanding** — conversation with the user (3–5 turns)
Stage 2 **Ideation** — generate scenario.yaml + weights.yaml
Stage 3 **Rollout** — invoke the runner CLI
Stage 4 **Judgment** — interpret the results.md for this specific use case

After Stage 4, always offer: *"Want to refine the scenario and re-run?"* This is the AdaTest-style inner loop.

## Stage 1 — Understanding

Goal: extract enough about the user's use case to fill in the scenario DSL.

**Turn 1 — examples, not criteria.** Ask:

> "Give me 1–2 concrete examples of things your agent's memory should keep and retrieve later, and 1–2 examples of things it should discard or at least de-prioritize. Don't worry about defining the rules — just the examples."

Rationale: EvalGen's "criteria drift" finding. Users can't define criteria upfront; they can recognize good/bad examples.

**Turn 2 — session shape.** Ask two short questions:

> "How many conversations/sessions does a typical user have with your agent before memory matters? And how long is one session — roughly how many turns?"

If the user is vague, offer defaults: 10 sessions × 40 steps. These are runner defaults.

**Turn 3 — taxonomy check.** Show the 4-family × 8-dimension matrix from references/taxonomy.md. Ask which 2–3 dimensions matter most for this use case. Do not force the user to rank all 8 — cognitive load is too high. You are looking for which *families* to weight.

**Turn 4 (optional) — archetype mix.** If the use case is ambiguous, show 3 candidate archetype mixes (see references/use-case-patterns.md), let the user pick or modify. Never show more than 3 candidates at once (AdaTest's 3–7 cap, we lean to 3).

By the end of Stage 1 you should know:
- Archetype mix: fractions for `core` / `evolving` / `episode` / `noise`
- Context evolution: `random` / `narrow-band-drift` / `stable` / `mode-shifts`
- Themes: 3–6 short lists of vocabulary tokens (ask the user for domain words if they're non-obvious)
- Which families they care about (for the Judgment stage)

If anything is ambiguous, default to the closest pattern in references/use-case-patterns.md and tell the user which pattern you chose and why.

## Stage 2 — Ideation

Write two files into the user's current working directory:
- `scenario-<name>.yaml` — the scenario config
- `weights-<name>.yaml` — family weights for Judgment (optional)

Use templates/scenario.yaml.tmpl and templates/weights.yaml.tmpl as starting points. Substitute the values from Stage 1.

Show the user the generated scenario.yaml and ask: *"Look right, or tweak anything before we run?"* Keep this confirmation to one round — don't re-litigate Stage 1.

## Stage 3 — Rollout

Invoke the runner via Bash:

```
memory-bench run --scenario scenario-<name>.yaml --out results/<name>/ --embedding --composite
```

The `--embedding` flag enables the sentence-transformers adapter (first run downloads ~90 MB model). The `--composite` flag enables the weighted multi-signal adapter. Both are recommended — without them you only get three cheap baselines and the leaderboard is thin.

The runner writes `results/<name>/results.md` and `results/<name>/results.json`. Read the markdown file.

Expected runtime: 1–5 minutes. If it's slower, sentence-transformers is doing a cold model download — this is normal on first run.

## Stage 4 — Judgment

Read results.md. Do not just paste it back to the user. Write a case-specific interpretation with three sections:

**1. Capability profile.** For each family the user said matters in Stage 1, state the winner, its score, and whether that score is high or low relative to the other scenarios in references/adapter-profiles.md. A winner with score 0.4 means "best available but still weak" — say that out loud.

**2. Tradeoffs observed.** Point to 1–2 dimensions where a non-winner adapter came close, and what that means. Example: *"Composite edges out Embedding in Update Coherence by 5%, but loses Personalization by 10%. For your use case, you care more about X, so Embedding is the safer default."*

**3. Recommended starting strategy.** One sentence: *"Start with <adapter> because <why>. If you see <symptom> in production, try <alternative>."* Be specific.

After these three sections, ask: *"Want to refine the scenario and re-run?"* Common refinements:
- Bump up an archetype fraction that felt underrepresented
- Switch context evolution type
- Add or remove themes
- Adjust weights.yaml to shift family priorities

## Key UX rules (full detail in references/elicitation-flow.md)

- **Grade before criteria** — ask for examples before asking for rules
- **Cap at 7** — never show more than 7 candidates/options/dimensions at once; prefer 3
- **Ranking always visible** — when you show candidates, show *why* they're ranked in that order
- **Iterate every 5–8 interactions** — surface pattern-detected summaries, don't let the conversation wander
- **Organization optional** — don't force a taxonomy on the user upfront; let structure emerge from the examples they give

## References

- references/taxonomy.md — the 4×8 matrix shown in Turn 3
- references/adapter-profiles.md — empirical profile of each strategy (what it wins, what it loses)
- references/use-case-patterns.md — canonical patterns (game / companion / RAG / coding)
- references/elicitation-flow.md — the UX rules above, with rationale
- examples/game-ai-walkthrough.md — a full game-AI scenario elicitation and result
- examples/npc-cognition-walkthrough.md — long-running NPC with stable persona
- examples/coding-agent-walkthrough.md — code/PR/design memory with frequent supersedes
- templates/scenario.yaml.tmpl — the scenario DSL skeleton
- templates/weights.yaml.tmpl — family weights skeleton

## What this skill does not do

- It does not call any LLM judges — all metrics are mechanical
- It does not evaluate actual agent responses — it evaluates the retrieval layer feeding them
- It does not benchmark external memory services (Mem0, Zep, Letta) — it benchmarks algorithmic primitives (Recency, BM25, ACT-R, Embedding, Composite)
- It does not replace production telemetry — it de-risks the initial strategy choice before you build
