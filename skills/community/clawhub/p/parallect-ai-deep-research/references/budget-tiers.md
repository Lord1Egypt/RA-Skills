# Parallect Budget Tiers Reference

Read this file when the user asks about pricing, budget options, or when
you need to recommend a tier for a specific research question.

## Tier Details

### XXS — Micro (~$1 max)
- **Providers:** 1 (cheapest available, typically Perplexity or Gemini Lite)
- **Mode:** Fast only (no synthesis)
- **Duration:** ~10-30 seconds
- **Best for:** Quick factual lookups, single-source verification
- **Output:** Raw single-provider report, no cross-referencing

### XS — Extra Small (~$2 max)
- **Providers:** 1-2
- **Mode:** Fast or methodical
- **Duration:** ~30s-2min
- **Best for:** Brief overviews, simple comparisons
- **Output:** Minimal synthesis if methodical

### S — Small (~$5 max)
- **Providers:** 2
- **Mode:** Fast or methodical
- **Duration:** ~1-3min
- **Best for:** Standard research questions, topic summaries
- **Output:** Basic synthesis with some cross-referencing

### M — Medium (~$15 max) [RECOMMENDED DEFAULT]
- **Providers:** 3-4
- **Mode:** Methodical recommended
- **Duration:** ~3-6min
- **Best for:** Detailed analysis, competitive research, technical topics
- **Output:** Full synthesis with claims, citations, conflict resolution

### L — Large (~$30 max)
- **Providers:** 4-5
- **Mode:** Methodical
- **Duration:** ~5-10min
- **Best for:** Comprehensive deep dives, regulatory research, due diligence
- **Output:** Extensive synthesis with high citation density

### XL — Extra Large (~$60 max)
- **Providers:** All available (5-6)
- **Mode:** Methodical
- **Duration:** ~8-15min
- **Best for:** Exhaustive research where no perspective should be missed
- **Output:** Maximum breadth, all providers contribute

## Tier Selection Heuristics

When helping the user choose a tier:

| Question complexity | Recommended tier |
|--------------------|-----------------|
| "What is X?" (factual) | XXS or XS |
| "Compare X and Y" (simple) | S |
| "What are the trends in X?" | M |
| "Analyze the implications of X for Y" | M or L |
| "Comprehensive review of X including regulatory, technical, and market aspects" | L or XL |

## Provider Strengths

Each provider has different strengths:

| Provider | Best at |
|----------|---------|
| Perplexity | Citation density, search breadth, speed |
| Gemini | Google Search grounding, structured data |
| OpenAI | Deep reasoning chains, nuanced analysis |
| Grok | Real-time X/social data, web search |
| Anthropic (Claude) | Synthesis quality, careful reasoning |

Higher tiers include more providers, giving broader coverage.
