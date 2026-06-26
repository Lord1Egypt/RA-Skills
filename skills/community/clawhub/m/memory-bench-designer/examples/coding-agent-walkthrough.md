# Worked example — Coding agent memory

A full conversation transcript for a coding agent's memory system: code/PR/design-decision memory across a multi-month project. Demonstrates the `mode-shifts` evolution pattern and high-`evolving` archetype mix.

## Use case

The user is building a coding agent that works on a multi-month software project. The agent needs to remember API shapes, design decisions, review comments, and recent commits — but these evolve constantly as the codebase changes. Work happens in focused bursts on different subsystems (auth for a week, then frontend, then infra).

## Stage 1 — Understanding

### Turn 1 (skill → user)

> Give me 1–2 examples of things your coding agent should keep in memory, and 1–2 it should discard.

### Turn 1 (user → skill)

> Keep: "the `AuthService.login()` signature changed from returning `Token` to returning `LoginResult` in PR #412". "The team decided to use Postgres over DynamoDB because of transaction requirements (ADR-03)". Discard: auto-generated migration files, log output from CI runs.

### Turn 2 (skill → user)

> Both of your "keep" examples are facts that will likely be superseded — signatures change, ADRs get revisited. This is the defining characteristic of coding-agent memory: most facts are *evolving*, not stable. How long is a typical project history you're spanning? And do you work on one subsystem at a time, or jump around?

### Turn 2 (user → skill)

> ~6 months of history. Usually I focus on one subsystem for days or weeks, then switch.

### Turn 3 (skill → user)

> Right — that's "mode-shifts" evolution: long stretches of focused work on one area, hard switches between subsystems. Given what you described, I'd prioritize **Maintenance** (does the agent correctly handle the signature-changed-in-PR-412 pattern?) and **Ranking** (when I ask "how does auth work?", is the top result the current answer, not the 6-month-old version?). Exploration and Adaptation less. Sound right?

### Turn 3 (user → skill)

> Yes. Maintenance is the #1 concern.

### Turn 4 (skill → user, pattern match)

> This matches our "Coding Agent" canonical pattern. Starting config:
>
> ```yaml
> archetypes:
>   core: 0.10      # project-wide conventions (rare)
>   evolving: 0.45  # function signatures, API shapes — supersede often
>   episode: 0.35   # commits, PRs, review comments
>   noise: 0.10     # generated files, log output
> context_evolution:
>   type: mode-shifts
>   drift_rate: 0.15
> themes: api, database, auth, frontend, infra
> ```
>
> The 45% `evolving` mix is the highest in our canonical patterns — it matches the "most facts supersede" observation. Confirm themes or swap them for your actual subsystems?

### Turn 4 (user → skill)

> Themes are close enough — my actual project has "api, database, auth, ui, deployment" but the benchmark is about structural properties so keep yours.

## Stage 2 — Ideation

`scenario-coding-agent.yaml` written (see runner/configs/scenario-coding-agent.yaml).

## Stage 3 — Rollout

```bash
memory-bench run --scenario scenario-coding-agent.yaml --out results/coding-agent/ --embedding --composite
```

Runtime: ~2 minutes.

## Stage 4 — Judgment

Skill reads results and writes:

> **Capability profile for your coding-agent memory:**
>
> - **Maintenance winner: Composite (0.68)** — your top-priority family. Update Coherence is 0.37 (the highest across adapters) and Forgetting Quality is 0.99. Update Coherence 0.37 sounds low; what it means is: when function signatures evolve, Composite correctly retrieves the new version *and partially suppresses* the old one, but perfect suppression is rare. In production, you may want to layer explicit version-tagging on top of retrieval.
> - **Ranking winner: Embedding (0.74)** — and this is tied for the highest Ranking score across our reference scenarios. Semantic queries about code ("how does auth work?") benefit from embeddings over token-matching because variable names and natural-language queries diverge. BM25 is a hair behind at 0.74 (virtually tied), so if embedding overhead is a problem in production you can fall back without losing signal.
>
> **Tradeoffs observed:**
>
> - Composite wins Maintenance by a 0.07 margin over Embedding (0.68 vs 0.61). That's the biggest family-winner margin in your scenario — the decay + importance weighting is doing real work against evolving signatures.
> - ACT-R wins Exploration at 0.55 but you said that's low-priority. Noted for completeness; don't pick ACT-R as your primary.
> - Recency is at 0.41 for Maintenance — meaningfully below Composite's 0.68. A pure-recency memory system would lose 40% of the Maintenance signal your scenario exposes.
>
> **Recommended starting strategy: Composite.**
>
> - It wins your headline family (Maintenance) and is within 0.06 of the Ranking winner.
> - If you observe stale facts leaking into top-K (the "LoginResult vs Token" problem resurfacing), the bottleneck is likely Update Coherence — 0.37 is the current ceiling. Layer explicit supersedes-links in your memory schema; retrieval alone won't get you to 1.0.
> - Budget alternative: BM25 + a supersedes-link layer. Gets you 95% of Composite's Maintenance with zero ML dependency.
>
> *Want to refine? Likely tweaks: bump `evolving` to 0.55 if your codebase churns even more, or switch to `random` evolution if the agent jumps across subsystems randomly rather than in multi-day bursts.*

## Actual empirical results

```
| adapter   | exploration | ranking | adaptation | maintenance |
| recency   | 0.424       | 0.282   | 0.163      | 0.409       |
| bm25      | 0.479       | 0.741   | 0.459      | 0.597       |
| actr      | 0.553       | 0.508   | 0.223      | 0.529       |
| embedding | 0.481       | 0.743   | 0.479      | 0.610       |
| composite | 0.524       | 0.676   | 0.418      | 0.680       |

Family winners:
- exploration → actr (0.553)
- ranking → embedding (0.743)
- adaptation → embedding (0.479)
- maintenance → composite (0.680)
```

## What this example demonstrates

- **Archetype mix matches problem structure.** 45% `evolving` is unusual — most use cases default to 10–20%. The user's description made it clear that most coding facts evolve, so the skill picked the right config instead of defaulting.
- **Mode-shifts evolution is rare.** It's the right fit when work happens in multi-day bursts on one topic. Most use cases are either narrow-band drift or stable; the skill correctly identified this scenario as the exception.
- **Judgment differentiated ceiling from ranking.** Composite wins Maintenance at 0.68, but Update Coherence alone is 0.37 — the Judgment decomposed the family score into its dimensions and recommended a production-level compensation (supersedes-links) rather than implying Composite is a complete solution.
- **Dev audience positioning.** This walkthrough speaks directly to the dev audience on GitHub. Unlike the game-AI or NPC walkthroughs, the evaluation criteria ("does the agent remember my refactor?") match what a developer would ask on their first use of the skill.
