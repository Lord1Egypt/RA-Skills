---
name: mac-maintenance
description: Inspect and maintain a Mac through repeatable terminal-first checks for disk usage, large files, launch agents, login items, power settings, sleep/wake behavior, networking, and OpenClaw health. Use when asked to clean up a Mac, diagnose slowness, inspect storage, review background processes, verify power or sleep settings, or produce a practical maintenance checklist for macOS.
---

# Mac Maintenance

Use terminal-first inspection. Prefer read-only checks before making changes. Summarize findings, then propose the smallest useful set of actions.

## Workflow

1. Clarify the scope if the request is broad: storage, performance, startup items, battery/power, networking, or OpenClaw health.
2. Run non-destructive inspection first.
3. Group findings into:
   - safe to report immediately
   - safe to fix automatically
   - risky changes that need confirmation
4. If making changes, prefer reversible actions and explain impact briefly.
5. End with a short maintenance summary and next steps.

## Common checks

### Storage and large files
- Inspect free space.
- Find unusually large files and folders.
- Separate cache/log growth from user documents.
- Suggest archival or cleanup before deleting anything.

### Background activity
- Inspect running processes, launch agents, and login items.
- Look for obvious resource hogs, crash loops, or stale helpers.
- Distinguish system services from third-party items.

### Power and sleep
- Inspect `pmset` settings, assertions, and recent sleep/wake logs.
- Use this path when diagnosing lid-close disconnects, overnight idle behavior, or caffeinate/disablesleep experiments.

### Networking
- Check interface status, local IPs, DNS, and reachability.
- For OpenClaw issues, also inspect `openclaw status` and relevant logs.

### OpenClaw-specific maintenance
- Run `openclaw status` when relevant.
- Check gateway health, channel state, update availability, and obvious warnings.
- Surface security warnings but do not change security-sensitive configuration without confirmation.

## Change policy

Safe without extra confirmation:
- inspection commands
- generating reports
- creating maintenance notes/scripts in the workspace

Ask before:
- deleting files outside obvious disposable caches
- changing startup items or launch agents
- changing power management settings
- installing or removing software
- changing firewall, SSH, or security settings

## Output pattern

When reporting results, use this structure:

- **What I checked**
- **What I found**
- **Recommended actions**
- **What I can do next**

Keep it practical. Avoid long generic Mac advice if the issue is specific.
