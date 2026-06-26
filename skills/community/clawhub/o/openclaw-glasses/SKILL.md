---
name: openclaw-glasses
description: Bilingual search-layer skill for OpenClaw that turns ordinary web lookup into multi-source retrieval, intent-aware ranking, adaptive weighting, thread-pulling research, Chinese-query optimization, and finance-aware realtime prioritization. Use when the user asks for web search, deep research, latest status/news, comparisons, resource finding, Chinese-language search, or realtime market data such as stocks, indices, forex, and crypto prices. Prefer this over raw web_search when you want broader coverage, better ranking, deeper context, or more reliable realtime quotes.
---

# OpenClaw Glasses

**See wider. Rank smarter. Answer with context.**

OpenClaw Glasses is a search layer for OpenClaw. It starts with ordinary web lookup, then adds multi-source retrieval, intent-aware reranking, adaptive weighting, optional thread-pulling research, Chinese-query optimization, and finance-aware realtime prioritization.

OpenClaw Glasses 是一个给 OpenClaw 用的“搜索层 / 增强检索层”。它不是简单叠加几个搜索源，而是把**多源召回、意图感知排序、权重自适应、链式追踪、中文优化、金融实时优先级**整合成一条完整检索链，让结果更接近“先找对，再排对，最后答对”。

## Public-facing summary

OpenClaw Glasses extends OpenClaw's native web tools into a smarter retrieval stack:
- **multi-source search** for broader recall and lower single-source bias
- **intent-aware search** for factual lookups, status/news, comparisons, tutorials, and exploratory research
- **adaptive weighting** so ranking changes with query type instead of using one fixed recipe
- **thread-pulling / follow-up research** for issues, discussions, and linked references
- **Chinese-query optimization** with CJK-aware matching and source weighting
- **finance-aware realtime prioritization** for stocks, indices, forex, and crypto quotes

OpenClaw Glasses 会把 OpenClaw 原生 web tools 扩展成一条更完整的检索链：
- **多源搜索**：扩大召回面，减少单一来源偏差
- **意图感知检索**：区分事实查询、状态更新、新闻、对比、教程、探索式研究
- **权重自适应**：不同问题走不同排序逻辑，而不是一套固定权重打天下
- **链式追踪 / 深挖**：遇到 issue、讨论帖、引用链时可以继续往下追
- **中文搜索优化**：针对中文查询做 CJK-aware 匹配与中文友好源加权
- **金融实时增强**：对股票、指数、外汇、加密资产等实时价格问题给出更稳的优先级

## Example triggers

- "帮我查一下 OpenClaw 最新进展，并按可靠性排序"
- "Compare Bun vs Deno for production backend use"
- "AAPL 最新股价"
- "BTC 实时价格和 24h 涨跌"

## Quick start

1. Use OpenClaw's built-in `web_search` as the agent-facing source when available.
2. Use `scripts/search.py` to aggregate additional providers and rerank results.
3. For status / exploratory / comparison work, prefer multi-query retrieval and intent scoring.
4. For finance price queries, let the finance-aware path boost Alpha Vantage and Binance results.

## What this skill adds

- Intent-aware search modes: factual, status, comparison, tutorial, exploratory, news, resource
- Multi-source aggregation: Exa, Tavily, Grok, Gemini, Kimi
- Chinese-query optimization:
  - CJK-aware keyword matching instead of space-splitting only
  - modest boosts for Chinese-friendly sources when the query is in Chinese
- Finance-aware weighting:
  - boosts Alpha Vantage for stocks / ETFs / forex / index proxies
  - boosts Binance for crypto realtime quotes
- Optional GitHub thread-pulling and reference extraction for deeper research

## Workflow

### 1. Pick the mode by intent

- Factual / tutorial → `answer` or light `deep`
- Status / news / comparison / exploratory → `deep`
- Resource finding → `fast`
- Finance realtime queries → `fast` for direct quote lookups, `deep` when combining quote + broader context

For intent examples and phrasing cues, read `references/intent-guide.md`.

### 2. Run the aggregator

Basic:

```bash
python3 scripts/search.py "query" --mode deep --intent exploratory --num 5
```

Multi-query comparison:

```bash
python3 scripts/search.py \
  --queries "Bun vs Deno" "Bun advantages" "Deno advantages" \
  --mode deep \
  --intent comparison
```

Finance quote:

```bash
python3 scripts/search.py "BTC 实时价格" --mode deep --intent status --source alpha-vantage,binance,gemini,kimi,tavily
```

### 3. Synthesize by topic, not by provider

- Answer first, then cite
- Group by themes or findings
- Call out conflicts explicitly
- Treat single-source or older claims more cautiously

## Scripts

### `scripts/search.py`
Primary multi-source retrieval and reranking entrypoint.

Capabilities:
- intent-aware scoring
- multi-query execution
- provider fusion
- Chinese-query weighting
- finance-aware realtime boosts
- optional extract-refs integration

### `scripts/fetch_thread.py`
Deep-fetch GitHub issues / PRs or generic pages to extract structured references.

### `scripts/chain_tracker.py`
Recursive thread-pulling / follow-up exploration with relevance gating.

### `scripts/relevance_gate.py`
Batch relevance filtering for candidate links.

## References

- `references/intent-guide.md` — intent cues and search-mode guidance
- `references/authority-domains.json` — authority weighting rules
- `references/research-light-regression-samples.md` — research-light behavior examples

## Configuration notes

Do not hardcode secrets in the skill.

Expected runtime configuration:
- search provider keys via environment or a local credentials file
- optional reuse of OpenClaw's existing web-search provider config
- finance sources should remain optional; degrade gracefully if unavailable

## Publishing / safety

Before packaging or publishing:
- remove all plaintext secrets
- remove machine-specific notes, personal paths, and private identifiers
- verify that examples and docs contain no local credentials or private data
- run the validator / packager before publishing
