# The 4-family × 8-dimension taxonomy

This is the cognitive scaffold you show the user in Stage 1, Turn 3. The two axes are orthogonal: families answer *"what capability?"*, dimensions answer *"how do we measure it?"*. Do not aggregate across families — a maintenance score and a ranking score measure different things and don't add up.

## The matrix

| Family | Dimension 1 | Dimension 2 |
|---|---|---|
| **Exploration** | Novelty Guarantee | Coverage |
| **Ranking** | Relevance @ K | Frequency Gain |
| **Adaptation** | Personalization | Cross-Session Learning |
| **Maintenance** | Update Coherence | Forgetting Quality |

## Families

### Exploration
*Does the memory system surface things the agent hasn't seen recently, or does it just keep returning the same stuff?*
High exploration matters when:
- The user has a large latent pool and you risk echo-chamber retrieval
- Serendipitous recall is valuable (companion agents, creative assistants)
- You want to avoid recency-bias collapse

### Ranking
*Given a query, does the memory system put the most relevant items at the top of top-K?*
High ranking matters when:
- Top-K is small (1–5) and ordering is load-bearing
- Queries are semantically rich (not keyword-matching)
- Production agent actually uses only the top few items

### Adaptation
*Does the memory system learn what this specific user/agent cares about over time, and carry that forward across sessions?*
High adaptation matters when:
- The agent has a persistent identity (NPCs, companions, personal assistants)
- User preferences matter more than population averages
- Cross-session continuity is a product requirement

### Maintenance
*When facts change or become noise, does the memory system update/forget coherently?*
High maintenance matters when:
- Facts supersede each other (codebase state, user preferences that evolve)
- Noise-to-signal ratio is high in the input stream
- The pool grows unbounded and must be pruned

## Dimensions

### Novelty Guarantee
Fraction of retrieved items that weren't in the previous retrieval set. Measures whether the strategy avoids returning the same items over and over. Filtered to relevance-positive items only (otherwise a strategy that returns random noise would score perfectly).

### Coverage
Fraction of observed items that ever appeared in *any* retrieval set across the run. Measures breadth of recall. Run-level, not step-level.

### Relevance @ K
NDCG-like score of the retrieved ranking against the ground-truth affinity to the query's theme. Rewards putting high-affinity items at the top. Position-discounted.

### Frequency Gain
Kendall-tau correlation between retrieval frequency (how often each item was retrieved) and ground-truth hit count (how often each item has affinity to queries seen so far). Measures whether often-relevant items are indeed retrieved often.

### Personalization
Overlap between per-theme retrieval histories. If the agent's queries about theme A over time produce a consistent set of items, personalization is high. Low personalization = retrieval shuffles every time.

### Cross-Session Learning
Fraction of late-session retrieval hits on items that were relevant in ≥2 prior sessions. Measures whether the system carries forward signal from prior sessions.

### Update Coherence
For `evolving` archetype pairs (v1 → v2), rewards retrieving v2 when both exist, with full credit only when v1 is suppressed entirely. Penalizes missing the pair altogether.

### Forgetting Quality
1 − fraction of retrievals that hit `noise` items. High when the strategy correctly deprioritizes zero-affinity items.

## How to present this to the user

Don't dump the whole matrix. Show the families first and ask which 2–3 matter. Then, for the chosen families, show the two dimensions per family and ask which ones resonate. Total cognitive load: pick 2–3 out of 4, then confirm the detail on those — never ask the user to rank 8 items at once.
