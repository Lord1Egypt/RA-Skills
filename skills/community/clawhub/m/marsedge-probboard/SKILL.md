---
name: marsedge-probboard
description: Query and summarize the MarsEdge probability board for BTC, ETH, SOL, and XRP 5-minute up/down signals. Use when the user asks for current probability board status, a quick board summary, the strongest coin, model-vs-market edge, Polymarket bid/ask comparison, short probability snapshots, or simple watchlist-style observations from marsedge.vip.
---

# MarsEdge ProbBoard

## Overview

Use this skill to read the live MarsEdge board and turn it into a concise trading-style summary.

The board is not for long essays. Default to a short, desk-style answer:
- strongest symbol(s)
- model up/down probability
- Polymarket bid/ask context
- where model and market seem misaligned
- obvious caveats when data is stale or missing

## Quick Start

Run the bundled fetch script first:

```bash
node /root/.openclaw/workspace/skills/marsedge-probboard/scripts/fetch-board.mjs
```

Optional base URL override:

```bash
node /root/.openclaw/workspace/skills/marsedge-probboard/scripts/fetch-board.mjs https://marsedge.vip
```

The script calls:
- `GET /api/probboard/latest`

and returns compact JSON for the board.

## Workflow

### 1. Fetch the board

Always fetch fresh board data before answering live-state questions.

If the API is unavailable, say so plainly and stop guessing.

### 2. Check freshness

Use `updatedAt`, `ts`, `ttl`, and `rem_secs` as sanity checks.

If data looks stale, say it is stale.

### 3. Rank what matters

Focus on:
- highest conviction probabilities
- biggest model vs market mismatches
- symbols with low remaining time when timing matters

Do not pretend tiny differences are meaningful.

### 4. Answer in trader format

Prefer a compact structure like:

- **Strongest up:** BTC 62.4%
- **Strongest down:** XRP 58.1%
- **Possible edge:** ETH up model 57% vs market ask 0.49
- **Caution:** SOL data is stale / countdown is low

## Edge Heuristic

Read `references/edge-rules.md` when the user asks for edge, opportunity, best coin, strongest setup, or a ranked summary.

Default interpretation:
- model up probability materially above market up ask → possible up-side value
- model down probability materially above market down ask → possible down-side value
- tiny differences are noise, not edge

## Output Style

Default to:
- short bullets
- direct numbers
- no fake certainty
- no table unless explicitly useful

Good example:

```text
当前盘面里最顺的是 BTC。
- BTC up 概率 61.8%，up ask 0.54，模型略偏多
- XRP down 概率更高，但盘口也不便宜，edge 没 BTC 干净
- SOL 剩余时间太短，别过度解读
```

## Resources

### scripts/
- `scripts/fetch-board.mjs` — fetch MarsEdge live board JSON

### references/
- `references/edge-rules.md` — concise heuristics for reading model-vs-market mismatch
