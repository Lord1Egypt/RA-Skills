# Local Agent Memory Architecture

## Core model

Use a layered file-based memory system:
- `memory/YYYY-MM-DD.md` for raw daily history
- `memory/semantic/` for stable facts and preferences
- `memory/procedural/` for repeatable workflows
- `MEMORY.md` as a lightweight index and routing layer

## Key disciplines

### Skeptical memory
Treat memory as a hint/index layer, not unquestionable truth.
If remembered information would cause a real action, re-check current files, paths, versions, scripts, or environment first.

### Strict write discipline
Write the destination topic file first.
Confirm success.
Only then update `MEMORY.md` if the information deserves long-term indexing.

### Lightweight summary
Keep `MEMORY.md` short and routing-oriented.
Put detail in topic files, not in the top-level summary.

### Consolidation
Use lightweight heartbeat-scale dream passes for routine cleanup.
Use deeper passes occasionally for heavy daily logs.
