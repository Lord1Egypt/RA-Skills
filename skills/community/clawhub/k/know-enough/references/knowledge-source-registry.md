# Knowledge Source Registry

A registry tells the agent **what a source means**, not just how to call it.

A registry entry never grants access; use only sources actually accessible within the task's authorization.

Prefer a project-level file such as `KNOWLEDGE_SOURCES.yaml`, but do not require one if the harness can discover sources dynamically.

For each source, describe:

- `description`: what the corpus contains;
- `role`: `authoritative`, `precedent`, `observational`, or `reference`;
- `use_for`: decisions/questions it is appropriate for;
- `avoid_for`: common misuse;
- `scope`: business/domain coverage;
- `freshness`: how current the content should be or how to interpret age;
- `adapter`: optional retrieval mechanism label;
- `target`: optional backend-specific corpus identifier.

## Role semantics

### authoritative
Current normative truth for the decision: approved policy, active specification, signed source of truth, official product reference.

### precedent
Historical examples that show what was done before. Precedent can inform judgment but does not grant current authority.

### observational
Evidence about what happened: logs, metrics, reports, transaction data.

### reference
Useful explanatory material without controlling authority.

## Selection rules

1. Pick sources by the information objective, not by vector similarity alone.
2. Prefer authoritative sources for “what is allowed/current/required?”
3. Prefer precedent for “has something similar been done before?”
4. Use observational data for “what actually happened?”
5. If source roles disagree, do not average them; explain the difference.
