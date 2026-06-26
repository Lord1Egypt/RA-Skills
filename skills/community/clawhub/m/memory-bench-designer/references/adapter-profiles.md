# Adapter profiles — what each strategy wins and loses

Empirical profiles from running all five adapters across three worked scenarios (game-ai, npc-cognition, coding-agent). Scores are 0–1, higher is better.

Use these profiles in Stage 4 (Judgment) to contextualize the user's results. A Personalization score of 0.7 means something different in a game-AI scenario vs an NPC scenario — these tables tell you what.

## Recency (null baseline)

Sorts by most-recent observation. No content understanding.

| Scenario | Exploration | Ranking | Adaptation | Maintenance |
|---|---|---|---|---|
| game-ai | 0.44 | 0.33 | 0.10 | 0.33 |
| npc-cognition | 0.30 | 0.31 | 0.08 | 0.41 |
| coding-agent | 0.42 | 0.28 | 0.16 | 0.41 |

**Wins:** basically nothing. It's the floor.
**When it surprises:** scenarios dominated by `episode` archetype with fast streaming arrival, where "what happened recently" is a decent proxy.
**Use as reference**: if your production strategy beats Recency by less than 0.15 on the family you care about, the strategy isn't earning its complexity.

## BM25 (statistical retrieval)

Token-overlap with k1=1.5, b=0.75. No embeddings.

| Scenario | Exploration | Ranking | Adaptation | Maintenance |
|---|---|---|---|---|
| game-ai | 0.38 | **0.70** | 0.45 | 0.60 |
| npc-cognition | 0.50 | 0.71 | 0.46 | 0.63 |
| coding-agent | 0.48 | 0.74 | 0.46 | 0.60 |

**Wins:** Ranking in narrow-band-drift scenarios (game-ai). Strong runner-up everywhere for Ranking.
**Where it ties Embedding:** when theme vocabularies don't overlap much. The more semantically crisp your themes, the closer BM25 gets to Embedding.
**When to pick it:** cheap and deterministic. No ML dependency, no embedding storage. Good first production baseline.

## ACT-R (cognitive activation)

Base-level activation `ln(1+count) × exp(-decay × age)`, with novelty bonus and semantic Jaccard.

| Scenario | Exploration | Ranking | Adaptation | Maintenance |
|---|---|---|---|---|
| game-ai | **0.54** | 0.45 | 0.26 | 0.47 |
| npc-cognition | **0.65** | 0.56 | 0.32 | 0.55 |
| coding-agent | **0.55** | 0.51 | 0.22 | 0.53 |

**Wins:** Exploration, consistently and by wide margins. NPC (stable theme) surfaces its strongest Exploration score because novelty still matters against a long-running single theme.
**Weakness:** Ranking and Adaptation. Its activation-based scoring doesn't carry semantic query-fit well enough to beat Embedding/BM25.
**When to pick it:** when exploration / coverage is the product requirement. Creative-assist agents, curiosity-driven NPCs, anti-echo-chamber retrieval.

## Embedding (semantic retrieval)

sentence-transformers/all-MiniLM-L6-v2, cosine via normalized dot product.

| Scenario | Exploration | Ranking | Adaptation | Maintenance |
|---|---|---|---|---|
| game-ai | 0.38 | 0.70 | **0.47** | 0.60 |
| npc-cognition | 0.49 | **0.74** | **0.49** | 0.67 |
| coding-agent | 0.48 | **0.74** | **0.48** | 0.61 |

**Wins:** Ranking in 2 of 3 scenarios, Adaptation in all 3. Wherever semantic queries matter more than keyword overlap.
**Loses to BM25:** game-ai Ranking. Narrow-band drift keeps vocabularies tight; BM25's token-matching catches it cleanly.
**When to pick it:** semantic search over your memory pool, queries phrased as sentences rather than keywords, production use case tolerates the ML dependency.

## Composite (weighted multi-signal)

0.5 × similarity + 0.3 × decay + 0.2 × importance. Wraps Embedding for similarity.

| Scenario | Exploration | Ranking | Adaptation | Maintenance |
|---|---|---|---|---|
| game-ai | 0.52 | 0.60 | 0.42 | **0.65** |
| npc-cognition | 0.51 | 0.63 | 0.44 | **0.69** |
| coding-agent | 0.52 | 0.68 | 0.42 | **0.68** |

**Wins:** Maintenance everywhere. Update Coherence and Forgetting Quality both benefit from decay and importance weighting.
**Balanced loser:** doesn't win Ranking or Adaptation outright (Embedding does), doesn't win Exploration (ACT-R does). But comes within 0.10 in every family except Adaptation.
**When to pick it:** when Maintenance is the family that matters — codebases with heavy superseding, long-running agents where noise accumulates, memory systems that need to prune aggressively.

## Family-winner matrix at a glance

| Family | game-ai (noise + drift) | npc-cognition (stable) | coding-agent (mode-shifts) |
|---|---|---|---|
| Exploration | ACT-R 0.54 | ACT-R 0.65 | ACT-R 0.55 |
| Ranking | **BM25 0.70** | Embedding 0.74 | Embedding 0.74 |
| Adaptation | Embedding 0.47 | Embedding 0.49 | Embedding 0.48 |
| Maintenance | Composite 0.65 | Composite 0.69 | Composite 0.68 |

## Reading this table in Judgment

The table shows that the *identity* of the winner changes across scenarios for Ranking (BM25 wins game-ai only). For the other three families, the winner is stable but the *magnitude* changes by up to 0.20. Both axes matter:

- **Winner change** (BM25 vs Embedding in game-ai): hard signal. Pick the winner.
- **Magnitude change** (ACT-R exploration 0.54 vs 0.65): soft signal. The same winner means something weaker in a harder scenario. Tell the user when their winner is weaker than the reference profile — their use case might need tuning, not just adapter selection.
