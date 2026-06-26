---
name: local-healthcheck
description: Simple local security check (firewall, updates, ssh status) without external dependencies.
metadata:
  openclaw:
    requires: []
---

# Local Healthcheck Skill

This skill provides a minimal security audit that can run on any macOS/Linux system without pulling external code.

## How to run
```
openclaw local-healthcheck run
```

It will:
1. Check if the firewall is enabled.
2. List open ports.
3. Verify that system software updates are up‑to‑date.
4. Show the status of the SSH daemon.
5. Write a short report to `memory/healthcheck-$(date +%F).md`.
"}