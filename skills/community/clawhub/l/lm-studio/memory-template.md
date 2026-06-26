# Memory Template — LM Studio

Create `~/lm-studio/memory.md` with this structure:

```markdown
# LM Studio Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation
- Auto-activate when:
- Explicit-only topics:
- Never activate for:

## Runtime Baseline
- OS:
- Hardware constraints:
- Preferred port:
- Server mode: app | llmster | undecided
- CLI available: yes | no

## Verified Models
- Chat:
- Coding:
- JSON or structured output:
- Embeddings:

## Known Good Checks
- Smoke test:
- Known-good context length:
- GPU preference:

## Incident Notes
- Date:
- Symptom:
- Root cause:
- Confirmed fix:

## Notes
- Stable user preference:
- Follow-up:

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still evolving | Keep learning from real LM Studio tasks |
| `complete` | Baseline is stable | Execute directly with minimal setup questions |
| `paused` | User paused extra profiling | Use the current baseline without pushing |
| `never_ask` | User opted out of setup | Never request setup context again |

## Principles

- Store verified runtime facts and outcomes, not vague guesses.
- Never store tokens, passwords, or copied credentials.
- Update `last` after meaningful runtime or model changes.
- Prefer short incident notes tied to one confirmed fix.
