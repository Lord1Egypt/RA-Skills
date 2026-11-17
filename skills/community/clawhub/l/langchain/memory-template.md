# Memory Template — LangChain

Create `~/Clawic/data/langchain/memory.md` with this structure:

```markdown
# LangChain Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Context
<!-- App shape: script, FastAPI service, worker, notebook -->
<!-- Which pieces exist: chains, agents, retrieval, evals, tracing -->
<!-- Installed versions if they were mentioned -->

## Pain Points
<!-- Failures they hit: streaming, parsing, agent loops, cost, upgrades -->

## Preferences
<!-- Depth of explanation, full files vs diffs -->
<!-- Stances not yet promoted to config.yaml keys -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning |
|-------|---------|
| `ongoing` | Still learning their stack and app shape |
| `complete` | Know their versions, providers, and deployment target |

Never record API keys, endpoints with embedded credentials, or prompt/document content that may contain customer data.
