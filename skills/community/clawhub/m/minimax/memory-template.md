# Memory Template - MiniMax

Create `~/minimax/memory.md` with this structure:

```markdown
# MiniMax Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
<!-- What the user is building with MiniMax and why -->
<!-- Example: Text plus speech workflow for narrated product demos with strict approval before media upload -->

## Activation Boundaries
<!-- When this skill should activate automatically and when it should stay quiet -->

## API Defaults
<!-- Native vs compatible interface choices, base routing notes, and auth expectations -->

## Modality Defaults
<!-- Preferred text models, speech defaults, media-job patterns, and output formats -->

## Safety and Cost
<!-- Budget boundaries, consent requirements, and no-go actions -->

## MCP Notes
<!-- Approved MCP hosts, scopes, and reasons they are allowed -->

## Notes
<!-- Durable operational observations worth reusing -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Default learning state | Keep refining durable MiniMax defaults |
| `complete` | Stable routing and trust posture | Reuse defaults unless the product surface changes |
| `paused` | User wants less overhead | Save only critical changes |
| `never_ask` | User rejected persistence | Operate statelessly |

## Key Principles

- Store workflow facts, not full prompts, full assets, or chat transcripts.
- Keep model names and interface choices exact when they affect reproducibility.
- Record consent and budget boundaries clearly for media and MCP work.
- Update `last` on each meaningful MiniMax session.
