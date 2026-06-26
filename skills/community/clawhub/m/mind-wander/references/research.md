# Research Foundations

## Core concept: hippocampal memory consolidation

The mind-wander agent is modelled on the hippocampal consolidation process:
during sleep and quiet periods, the hippocampus replays and integrates recent
experiences, cross-referencing them with existing knowledge. Only genuinely novel
associations are elevated to cortical long-term memory — most processing is discarded.

This maps directly to the agent's architecture:
- ON_YOUR_MIND.md = recent working memory / unresolved questions
- Wander sessions = background consolidation passes
- Dead ends = correctly discarded associations (don't waste time again)
- MENTAL_EXPLORATION.md = elevated novel associations
- memwatchd → graph-rag = cortical integration

## Key papers

### Mind-wandering cognitive science
- Christoff et al. (2016). *Mind-wandering as spontaneous thought: a dynamic framework.*
  Nature Reviews Neuroscience. https://doi.org/10.1038/nrn.2016.113
  The default mode network (DMN) underpins spontaneous thought — our agent approximates
  this with scheduled autonomous reasoning.

### Hippocampal consolidation
- Frankland & Bontempi (2005). *The organization of recent and remote memories.*
  Nature Reviews Neuroscience. https://doi.org/10.1038/nrn1607
  Two-stage memory consolidation: hippocampal (recent, fast) → neocortical (remote, slow).
  Motivates the recency→semantic blend in graph-rag-memory's brief generation.

### RouterRetriever (foundational for graph-rag-memory integration)
- Zhuang et al. (2025). *RouterRetriever: Exploring the Benefits of Routing over Multiple
  Expert Embedding Models.* AAAI 2025. https://arxiv.org/abs/2409.02685
  Centroid-based routing outperforms learned classifiers for domain expert selection.
  Used in the companion graph-rag-memory skill.

### Novel finding from this system

**Cross-space routing robustness (2026-04-04, first finding):**
The mind-wander agent independently discovered and empirically tested that routing
queries via one embedding space (nomic-embed-text, 768-dim) then retrieving via a
different space (arctic-embed2/bge-m3, 1024-dim) achieves the same accuracy as
single-space routing. Domain-level routing is robust to embedding space discontinuities.
This appears to be unstudied — no paper found after 30+ targeted searches.
See NOVELTY_LOG.md for full details and publication path.

## Design decisions

### Why a local model?
Qwen3.5-9B runs entirely on local GPU. Zero API costs for background reasoning.
The v2 distillation specifically targets reasoning economy — it produces concise
reasoning chains, critical for background agents that must decide quickly whether
something is worth elevating.

### Why a separate wander graph?
The wander graph (FalkorDB 'wander') is invisible to the primary agent. Dead ends,
session history, and exploration chains never pollute the primary context. Only
elevated findings cross the boundary via MENTAL_EXPLORATION.md → memwatchd.

### Why the novelty gate matters
A background agent that writes everything it finds would drown the primary agent
in noise. The strict novelty gate — requiring something genuinely new, not just
a restatement of known facts — is the critical design decision that makes the
system useful rather than distracting.
