---
name: gsd-pi
description: >
  Redirect — install `gsd-orchestrator` instead.
  This skill exists to reserve the name. The full orchestration skill
  with subprocess patterns, exit code handling, and HeadlessJsonResult
  documentation lives at `gsd-orchestrator`.
metadata:
  openclaw:
    requires:
      bins: [gsd]
    install:
      kind: node
      package: gsd-pi
      bins: [gsd]
---

# gsd-pi → gsd-orchestrator

> **This is a name reservation. Install [`gsd-orchestrator`](https://clawhub.com/skills/gsd-orchestrator) instead.**

The `gsd-orchestrator` skill provides complete subprocess-based orchestration patterns for GSD projects:

- Milestone creation from specs
- Task execution via `gsd headless`
- Status polling and blocker handling
- Cost tracking and budget enforcement
- Exit code interpretation (0/1/10/11)
- HeadlessJsonResult JSON parsing

## Install the real skill

```bash
clawhub install gsd-orchestrator
```
