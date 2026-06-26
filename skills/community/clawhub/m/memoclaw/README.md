# MemoClaw Skill

Persistent semantic memory for AI agents. Store facts, recall them later with natural language. No API keys — your wallet is your identity.

**Install:** `clawhub install memoclaw`

## 30-second quickstart

```bash
npm install -g memoclaw
memoclaw init                    # one-time wallet setup
memoclaw store "User prefers dark mode" --importance 0.8 --memory-type preference
memoclaw recall "UI preferences"  # semantic search
```

## How it works

1. **Store** facts with importance scores, tags, and memory types
2. **Recall** with natural language — vector search finds semantically similar memories
3. **Decay** naturally — memory types control half-lives (corrections: 180d, observations: 14d)
4. **Pin** critical facts so they never decay

Every wallet gets **100 free API calls**. After that, embedding-backed commands pay per call: store/update/recall/batch update stay at $0.005 while context/extract/ingest/consolidate/migrate cost $0.01. List/get/search/core/etc remain free. (USDC on Base)

## What agents get

| Feature | Details |
|---------|---------|
| Semantic recall | "What editor does the user prefer?" → finds "User likes Neovim with vim bindings" |
| Free-tier first | `core` + `search` are free; `recall` + `context` only when needed |
| Auto-dedup | `consolidate` merges similar memories |
| Namespaces | Isolate memories per project |
| Relations | Link memories: supersedes, contradicts, supports |
| Import/export | Migrate from MEMORY.md files, export as JSON/CSV/markdown |

## Key commands

```bash
memoclaw store "fact" --importance 0.8 --memory-type preference   # $0.005
memoclaw recall "query" --limit 5                                  # $0.005
memoclaw core --limit 5                                            # FREE
memoclaw search "keyword"                                          # FREE
memoclaw list --sort-by importance --limit 10                      # FREE
memoclaw context "what I need" --limit 10                          # $0.01
memoclaw consolidate --namespace default --dry-run                 # $0.01
memoclaw stats                                                     # FREE
```

## Cost

| Usage | Daily cost | Monthly |
|-------|-----------|---------|
| Light (3-5 paid calls/day) | ~$0.02 | ~$0.60 |
| Moderate (10-20/day) | ~$0.08 | ~$2.40 |
| Heavy (30-50/day) | ~$0.20 | ~$6.00 |

Many commands are free: list, get, delete, search, core, stats, tags, history, export, and more. Only embedding-backed calls (store/update/recall/context/extract/ingest/consolidate/migrate) incur the paid per-call pricing.

### Cost tiers after the free 100 calls

| Tier | Price | Commands and notes |
|------|-------|--------------------|
| Free | $0 | list, get, delete, bulk delete, search (text), core, suggested, relations, history, export, namespace list/stats, count, browse, config, tags, watch, alias, snapshot, pin/unpin, lock/unlock, edit, copy, move, whoami, status, upgrade (see note<sup>3</sup>) |
| Embedding | $0.005 per call<sup>1</sup> | store, store --file, store --batch<sup>2</sup>, update (when content changes), recall, batch update |
| Workflow | $0.01 per call | context, extract, ingest, consolidate, migrate |

1. Update only bills when you change the stored content (metadata-only edits stay free). Recall and store charges include the embedding regeneration.
2. Batch store costs $0.04 per request for up to 100 memories and draws from the same $0.005 embedding tier.
3. See SKILL.md for the exhaustive list of free commands if you need something beyond the highlights above.


## Resources

- [SKILL.md](SKILL.md) — Full agent instructions, decision trees, and CLI reference
- [examples.md](examples.md) — 13 detailed usage scenarios with cost breakdowns
- [api-reference.md](api-reference.md) — HTTP endpoint documentation
- [Docs](https://docs.memoclaw.com) · [Website](https://memoclaw.com) · [ClawHub](https://clawhub.ai/anajuliabit/memoclaw)

## License

MIT
