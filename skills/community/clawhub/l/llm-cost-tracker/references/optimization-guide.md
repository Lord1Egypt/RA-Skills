# API Cost Optimization Guide

## Model Selection Matrix

| Task Type | Recommended Model | Cost/1M tokens | vs. Opus savings |
|-----------|------------------|----------------|-----------------|
| Classification/routing | Haiku 3.5 / GPT-4o-mini | $0.15-$0.80 | 95% |
| Simple extraction | Haiku 3.5 / Flash 2.0 | $0.10-$0.80 | 95% |
| Code generation | Sonnet 4 / GPT-4o | $3.00 | 80% |
| Complex reasoning | Opus 4 / o3 | $15-$75 | baseline |
| Summarization | Sonnet 4 / Flash 2.0 | $0.40-$3.00 | 80-97% |

## Caching Strategies

### Anthropic Prompt Caching
- Cache system prompts (saves 90% on repeated calls)
- Cache large documents in the first message
- Cache tool definitions
- Break-even: 2+ uses of same cached content

### Local Response Caching
- Hash input prompts and cache outputs for identical queries
- TTL: 1 hour for dynamic data, 24 hours for static analysis
- Storage: SQLite DB at `~/.openclaw/cache/responses.db`

## Context Window Management

### Aggressive Trimming
- Keep only last 3-5 turns in conversation history
- Summarize older context instead of including verbatim
- Remove tool call details from history (keep results only)

### Lazy Skill Loading
- OpenClaw loads skill descriptions (~100 words) always
- Full SKILL.md only loads when triggered
- Minimize skill description length to reduce base cost

## Monitoring Cadence

- **Daily**: Check spend vs. daily budget
- **Weekly**: Review per-model breakdown, identify downgrade opportunities
- **Monthly**: Full optimization review, update model routing rules
