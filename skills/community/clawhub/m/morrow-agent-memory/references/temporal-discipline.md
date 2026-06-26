# Temporal Memory Discipline

Lightweight conventions for adding temporal validity to flat memory files — without a full knowledge graph.

## Core Convention

Add `[YYYY-MM-DD]` timestamps to every significant fact in memory files. When a fact is superseded, mark it explicitly rather than deleting it.

### Example: config fact that changed

```markdown
## Telegram Channel

- [2026-03-27] Status: ENABLED. Account "Morrow Operator Bot". dmPolicy: pairing.
  - ~~[2026-03-20] Status: DISABLED~~ SUPERSEDED 2026-03-27 (config updated)
```

### Example: tool capability verified

```markdown
## Verified Tools

- [2026-03-27] /v1/embeddings: 768-dim, model="openclaw", auth via gateway token ✓
- [2026-03-27] /v1/chat/completions: Claude Sonnet 4.6 via Bedrock, ignores response_format ✓
- [2026-03-26] context7-mcp: npx -y @upstash/context7-mcp, no auth, 5048 OpenClaw snippets ✓
```

## Why This Matters

Without timestamps, memory files suffer **silent staleness**. A fact written in March that's been superseded in April looks identical to a current fact. The agent propagates stale beliefs confidently.

With timestamps:
- The agent can evaluate freshness before acting on a fact
- The human auditing the memory can see when facts were established
- Supersession is legible rather than hidden

## SUPERSEDES Pattern

When writing a new fact that replaces an old one:

```markdown
- [YYYY-MM-DD] <new fact> — SUPERSEDES [prior-date] entry
```

Do NOT silently delete the old entry if it was significant. This preserves the audit trail.

## Temporal Query Discipline

Before trusting a memory fact for a consequential action:
1. Check the timestamp — is it more than a week old?
2. Is it in RUNTIME_REALITY.md (live state) or a static memory file?
3. For infrastructure/channel facts: re-verify via `openclaw status` or equivalent

Facts in RUNTIME_REALITY.md should be verified at each rotation, not inherited stale.
