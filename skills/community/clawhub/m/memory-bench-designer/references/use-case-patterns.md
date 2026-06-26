# Canonical use-case patterns

When the user's use case is ambiguous, match it to one of these four patterns and tell them which pattern you picked. Each pattern is a starting point for the scenario DSL — users can tweak from there.

## Pattern: Game AI (action / stealth / combat)

**Signature**: short-lived episodic memories, high noise, narrow-band theme drift within a gameplay session.

```yaml
archetypes:
  core: 0.15      # stable facts about the world/player
  evolving: 0.10  # rarely changes mid-session
  episode: 0.40  # streaming gameplay events
  noise: 0.35    # background chatter, irrelevant events
context_evolution:
  type: narrow-band-drift
  drift_rate: 0.25
  themes: 5       # gameplay modes: stealth/combat/exploration/social/crafting
```

**Why these numbers**: gameplay sessions generate streams of low-value events (noise), occasional high-value tactical moments (episode), and stable world knowledge (small core). Themes drift as the player switches modes — narrow-band, not random.

**Expected winner profile**: ACT-R (Exploration, high novelty), BM25 (Ranking — vocab is tight), Composite (Maintenance — need to forget noise).

## Pattern: NPC Cognition / Companion Agent

**Signature**: long-running identity, stable theme, facts accumulate and occasionally supersede.

```yaml
archetypes:
  core: 0.45      # persona facts, values, long-term traits
  evolving: 0.10  # occasional preference updates
  episode: 0.30   # specific memorable interactions
  noise: 0.15    # small talk, irrelevant exchanges
context_evolution:
  type: stable
  drift_rate: 0.1
  themes: 5       # identity/skills/relationships/values/goals
```

**Why these numbers**: an NPC or companion agent's memory is dominated by stable identity facts (high core). Conversations return to the same themes over and over (stable evolution). Some interactions matter as episodes. Noise is low because players/users filter their input before talking to a persistent agent.

**Research-lineage context**: this pattern is motivated by embodied-NPC cognitive architectures (e.g. FEP-based embodied NPC runtimes). Those systems need memory that carries identity across sessions — which is exactly what Adaptation and Cross-Session Learning measure.

**Expected winner profile**: ACT-R (Exploration, highest magnitude of any scenario), Embedding (Ranking + Adaptation, semantic queries about stable themes), Composite (Maintenance).

## Pattern: Coding Agent (codebase memory)

**Signature**: facts get superseded constantly, mode shifts between subsystems, low noise.

```yaml
archetypes:
  core: 0.10      # project-wide conventions
  evolving: 0.45  # function signatures, API shapes — supersede often
  episode: 0.35   # commits, PRs, review comments
  noise: 0.10    # irrelevant files / generated output
context_evolution:
  type: mode-shifts
  drift_rate: 0.15
  themes: 5       # api/database/auth/frontend/infra
```

**Why these numbers**: in a multi-month codebase, most facts are of `evolving` type (function signatures change, API shapes change, designs change). Work happens in focused mode-shifts between subsystems (you work on auth for two days, then frontend for a week). Noise is low because the codebase is mostly signal.

**Expected winner profile**: Embedding (Ranking — rich queries), Composite (Maintenance — update coherence is the headline dimension).

## Pattern: RAG / Document Q&A

**Signature**: large stable pool, random access, little temporal structure.

```yaml
archetypes:
  core: 0.55      # the corpus is mostly stable
  evolving: 0.15  # documents get revised
  episode: 0.20   # query-specific context
  noise: 0.10
context_evolution:
  type: random
  drift_rate: 0.5
  themes: 6       # whatever your corpus categorization is
```

**Why these numbers**: RAG corpora don't drift — users query random parts of a stable document set. High core, random evolution, low noise (assumed clean corpus).

**Expected winner profile**: Embedding dominates. If your RAG system doesn't embed, BM25 is the floor.

## How to use these patterns

- **Ask the user to pick one.** "Your use case sounds closest to <pattern>. Here's the archetype mix I'd start with. Look right, or should we adjust?"
- **Never pick silently.** If you match the user to `NPC Cognition` and the user was actually describing a game-AI scenario, that's a 2-turn waste. Tell them which pattern you picked so they can redirect.
- **The patterns are starting points, not prescriptions.** A hybrid (e.g. coding-agent archetypes + RAG-style random context evolution) is fine if the user asks for it.

## When none of the patterns fit

If the user describes something that doesn't match any of the four, ask them the raw DSL questions directly:
- *"Out of every 100 memories, roughly how many are stable facts vs things that change vs one-off episodes vs noise?"* → archetype fractions
- *"Do conversations stay on one topic, drift between adjacent topics, switch in chunks, or jump around randomly?"* → context evolution type
- *"What are the 3–6 main themes or topics in your memory pool?"* → themes list

Get best-effort answers, write the YAML, and flag the novelty: *"This scenario doesn't match our four canonical patterns — we're flying blind on what to expect. The results will still be valid; we just can't cross-reference against the adapter profiles as cleanly."*
