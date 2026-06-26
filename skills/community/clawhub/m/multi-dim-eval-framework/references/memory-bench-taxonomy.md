# Sister Case: memory-bench-designer's 4-Family × 8-Dimension Taxonomy

This document shows how the multi-dim eval pattern applies to a completely different domain: memory strategy benchmarking. The MADEF axes (see [madef-axes.md](madef-axes.md)) target multi-agent deliberation; this taxonomy targets agent memory retrieval. Same pattern, different instantiation.

If you're designing your own framework, comparing these two instantiations helps see which choices are pattern-fixed (group structure, canonical/proxy duality) vs domain-specific (which families, which dimensions).

Source: `memory-bench-designer/skill/references/taxonomy.md`. Published as a Claude Skill in 2026-Q2; runs across 5 memory adapters (Recency, BM25, ACT-R, Embedding, Composite) on 3 worked scenarios (game-AI, NPC cognition, coding agent).

---

## The 4×2 matrix

| Family | Dimension 1 | Dimension 2 |
|---|---|---|
| **Exploration** | Novelty Guarantee | Coverage |
| **Ranking** | Relevance @ K | Frequency Gain |
| **Adaptation** | Personalization | Cross-Session Learning |
| **Maintenance** | Update Coherence | Forgetting Quality |

---

## Families

### Exploration
*Does the memory system surface things the agent hasn't seen recently, or does it just keep returning the same stuff?*

High exploration matters when the agent has a large latent pool and risks echo-chamber retrieval, or when serendipitous recall is product-valuable.

### Ranking
*Given a query, does the memory system put the most relevant items at the top of top-K?*

High ranking matters when top-K is small (1-5), ordering is load-bearing, queries are semantically rich (not keyword-matching).

### Adaptation
*Does the memory system learn what this specific user/agent cares about over time, and carry that forward across sessions?*

High adaptation matters when the agent has persistent identity (NPCs, companions, personal assistants), user preferences matter more than population averages, cross-session continuity is a product requirement.

### Maintenance
*When facts change or become noise, does the memory system update/forget coherently?*

High maintenance matters when facts supersede each other, noise-to-signal ratio is high in the input stream, the pool grows unbounded and must be pruned.

---

## Dimensions (concise)

- **Novelty Guarantee** — fraction of retrieved items not in the previous retrieval set. Filtered to relevance-positive items only.
- **Coverage** — fraction of pool items ever retrieved across the run. Run-level, not step-level.
- **Relevance @ K** — NDCG-like score of the retrieved ranking against ground-truth affinity.
- **Frequency Gain** — Kendall-tau between retrieval frequency and ground-truth hit count.
- **Personalization** — overlap between per-theme retrieval histories.
- **Cross-Session Learning** — fraction of late-session hits on items relevant in ≥2 prior sessions.
- **Update Coherence** — for `evolving` archetype pairs (v1 → v2), retrieve v2 with full credit only when v1 is suppressed.
- **Forgetting Quality** — `1 − fraction of retrievals that hit noise items`.

---

## Cross-comparison: MADEF vs memory-bench-designer

Both follow the multi-dim eval pattern. Where they align and diverge:

| Property | MADEF | memory-bench-designer |
|---|---|---|
| Domain | Multi-agent deliberation evaluation | Agent memory strategy benchmarking |
| Group count | 3 (Grounding / Dynamics / Architecture) | 4 (Exploration / Ranking / Adaptation / Maintenance) |
| Dimension count | 12 | 8 |
| Canonical/proxy duality | Yes (each axis has both) | Partial (canonical only; no formal proxy) |
| Family axes orthogonal? | Mostly (some coupling A1↔A3) | Yes (designed orthogonal) |
| Composite forbidden | Yes | Yes |
| Calibration cases | v5 / v6a / v6b / v7 deliberation experiments | game-ai / npc-cognition / coding-agent reference scenarios |
| Versioning | v0 → v1 frozen post-calibration with logged iterations | v0.1 → v0.2 with normalized leaderboard added |
| Adversarial measurement | Stress rounds with forced absence | Random baseline subtraction (normalized score) |

### Pattern-fixed elements (both share)

- Multi-group structure to forbid composite
- Canonical formal definitions per dimension
- Calibration cases with expected ordinals
- Failure mode transparency
- Versioning with iteration log
- The reader is forced to look at multiple numbers, not one

### Domain-specific elements (each has its own)

- Which families/dimensions matter (deliberation cares about Grounding; memory cares about Exploration)
- Whether dimensions need normalization for population (deliberation: yes for agent count; memory: not needed because protocol is fixed)
- Whether stress testing exists (deliberation: yes via forced absence; memory: no — but baseline subtraction serves a related role)

---

## A subtle technique from memory-bench: random baseline subtraction

memory-bench v0.2 added a "normalized leaderboard": `(raw − random_baseline) / (1 − random_baseline)`.

Why this matters: a high *raw* score in a noisy scenario (e.g., `forgetting_quality` raw 0.70 in a 10%-noise scenario) doesn't mean the strategy works — a random adapter in that scenario gets 0.90 (it gets 90% lucky on noise). The strategy is *worse than random* despite the apparently high score.

The normalized score (clamped [-1, 1]) makes this visible: 0 means "matches a random adapter on that dimension", positive means real signal, negative means strictly worse than random.

**MADEF doesn't have this** — its dimensions are mostly process-quality, not retrieval-quality, so random baseline doesn't apply. But the principle generalizes: **whenever a high raw score could be achieved by chance or by saturation, subtract the floor.** This is one form of the "failure-mode transparency" principle from [group-design-principles.md](group-design-principles.md).

---

## Why this matters when designing your own framework

Two takeaways:

1. **The group structure is yours to design.** MADEF has 3 groups because deliberation has those 3 layers (evidence / process / structure). memory-bench has 4 because memory has those 4 capability axes. Don't force a 3-group answer — let the domain dictate the grouping.

2. **The canonical/proxy split is more useful in some domains than others.** MADEF has it because deliberation experiments span infrastructure generations. memory-bench less needs it because all benchmarks run with identical instrumentation. If your domain has cross-generation comparisons, build canonical/proxy in. If it's all on the same harness, you may skip proxy and rely on baseline subtraction instead.

The pattern (multi-group + canonical-explicit + group-wise reporting) generalizes; the specific shape depends on what you're evaluating.

---

## Reference: family-winner matrix from memory-bench (illustrative)

| Family | Scenario A (noise + drift) | Scenario B (stable) | Scenario C (mode-shifts) |
|---|---|---|---|
| Exploration | ACT-R 0.54 | ACT-R 0.65 | ACT-R 0.55 |
| Ranking | **BM25 0.70** | Embedding 0.74 | Embedding 0.74 |
| Adaptation | Embedding 0.47 | Embedding 0.49 | Embedding 0.48 |
| Maintenance | Composite 0.65 | Composite 0.69 | Composite 0.68 |

Note that Ranking's winner *changes* across scenarios (BM25 wins Scenario A but loses elsewhere). The other three families have a stable winner but the *magnitude* changes. Both axes (winner-stability and magnitude-shift) carry signal — and a single composite would erase both.

This is the kind of artifact a well-designed multi-dim framework produces. The final user doesn't get "best memory adapter overall"; they get "for your specific scenario, here's which adapter wins which family, and here's how confident we are."
