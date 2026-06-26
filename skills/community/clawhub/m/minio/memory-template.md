# Memory Template - MinIO Operations

Create `~/minio/memory.md` with this structure:

```markdown
# MinIO Operations Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Activation Preferences
- Auto-activation boundaries for MinIO and S3-compatible operations
- Ask-first versus proactive behavior by risk level
- Environments where auto-activation is restricted

## Environment Context
- Endpoint aliases, deployment mode, and region conventions
- Storage topology and capacity constraints
- Encryption and TLS baseline decisions

## Buckets and Data Controls
- Bucket inventory and high-risk prefixes
- Versioning, object lock, retention, and lifecycle expectations
- Replication scope and validation cadence

## Identity and Access
- User and group policy boundaries
- Key rotation cadence and ownership
- Audit and least-privilege decisions

## Incident Patterns
- Recurring failure signatures
- Confirmed rollback and recovery procedures
- Post-incident hardening actions

## Notes
- Durable context that improves future operations

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still evolving | Keep collecting context during normal work |
| `complete` | Core environment context is stable | Execute quickly with minimal clarification |
| `paused` | User paused setup prompts | Continue tasks using existing context |
| `never_ask` | User does not want setup prompts | Do not ask setup questions unless requested |

## Memory Principles

- Keep entries factual and tied to operational decisions.
- Replace stale assumptions instead of stacking contradictions.
- Save reusable context only, not one-off task chatter.
- Never store secrets, raw keys, or unrelated personal data.
- Update `last` after each meaningful execution.
