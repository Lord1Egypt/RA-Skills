# Memory Template — Paperclip

Create `~/paperclip/memory.md`:

```markdown
# Paperclip Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Environment
<!-- API base, local data dir, deployment mode, auth mode -->

## Company Scope
<!-- Active companies, goals, key projects, and responsible operators -->

## Adapter Defaults
<!-- Preferred runtimes, host boundaries, Docker notes, wake patterns -->

## OpenClaw Notes
<!-- Gateway URL, Docker hostname caveats, invite workflow status -->

## Notes
<!-- Repeated blockers, successful commands, and operator preferences -->
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning the setup | Add context when it reduces future friction |
| `complete` | Stable enough to operate | Reuse stored defaults before asking |
| `paused` | User wants no setup discussion now | Work with current facts only |
| `never_ask` | User opted out of setup prompts | Never ask unless explicitly requested |

## Key Principles

- Keep secrets out of memory files.
- Store environment facts and operating preferences, not raw tokens.
- Update `last` whenever the skill is used meaningfully.
