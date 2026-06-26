# Memory Template - Ollama

Create `~/ollama/memory.md` with this structure:

```markdown
# Ollama Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- What the user is trying to run and why -->
<!-- Example: Local coding assistant on a MacBook Pro with strict local-only privacy -->

## Environment
<!-- Host type, OS, GPU or CPU-only constraints, service manager, remote or local use -->

## Model Defaults
<!-- Preferred model tags, copied aliases, context sizes, and when to use each -->

## API and Modelfile Defaults
<!-- Base URLs, JSON reliability rules, named custom models, and prompt-layer decisions -->

## RAG and Retrieval
<!-- Embedding model choice, chunking defaults, vector dimensions, and retrieval checks -->

## Notes
<!-- Durable operational observations worth reusing -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Default learning state | Keep refining durable Ollama context |
| `complete` | Stable setup and defaults | Reuse defaults unless the environment changes |
| `paused` | User wants less overhead | Save only critical updates |
| `never_ask` | User rejected persistence | Operate statelessly |

## Key Principles

- Store workflow facts, not full prompts or chat transcripts.
- Keep model names exact when they affect reproducibility.
- Note the difference between local-only and optional cloud paths.
- Update `last` on each meaningful Ollama session.
