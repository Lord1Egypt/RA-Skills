---
name: lobster-workspace-guardian
description: Enforce consistent workspace structure, naming, memory tiering, and safety boundaries for AI agents. Use when: (1) creating, organizing, or verifying file/folder placement, (2) managing memory files and knowledge base entries, (3) setting up new projects, (4) cleaning up temporary or scattered files, (5) enforcing naming conventions, (6) running reusable scripts for validation or cleanup. Triggers: "organize workspace", "clean up", "where should I save", "naming convention", "memory archive", "project setup", "scattered files".
---

# Workspace Guardian

> Enforce workspace discipline — consistent structure, naming, memory lifecycle, and safety boundaries.

---

## Quick Reference

```
workspace/
├── projects/   YYYYNNNN_name     — source code only
├── knowledge/  topics|articles|research|assets — knowledge files only
├── output/     wechat|docs|slides|preview — final deliverables
├── memory/     YYYY-MM-DD.md → archive/ (14d+) — never deleted
├── logs/       run-time logs
├── .temp/      temporary files — delete after use
└── slides/     presentations
```

---

## Core Rules (6 Tenets)

### 1. System Files Stay Outside

No workspace files in OpenClaw's own directories (`~/.openclaw/` except `workspace/`, `~/.openclaw/canvas/`, etc.).

### 2. Workspace Is the Only Writable Zone

All AI-generated files → `workspace/` subtree only. Never write to `Desktop/`, `Downloads/`, `~/`, or system paths.

### 3. Scattered Files → Immediate Redirect

Any file not in its designated directory → move to correct location, not delete.

### 4. One Config Backup Only

Configuration or `.json`-based projects keep one archived/expired backup, not piles of timestamps.

### 5. Temp Files → Never Overnight

`.temp/` files: delete after task completion. >7 days stale → cleanup on next session start.

### 6. Skills Source Separation

ClawHub-installed skills in `skills/`. User-built local skills also in `skills/`. No double installation.

---

## File Routing Rules

| Content Type | Destination |
|---|---|
| Source code/projects | `projects/YYYYNNNN_name/` |
| Knowledge/research | `knowledge/topics|articles|research|assets/` |
| WeChat articles | `output/wechat/` |
| Word/PDF docs | `output/docs/` |
| Presentations | `output/slides/` |
| Preview files | `output/preview/` (delete after publish) |
| Daily logs | `memory/YYYY-MM-DD.md` |
| Temp work | `.temp/temp_*` (delete after use) |

---

## Naming Standards

| Rule | Pattern |
|---|---|
| Project dirs | `YYYYNNNN_project-name` |
| Output files | `{description}_v1\|v2\|final.{ext}` |
| Avoid | spaces, Chinese characters in dir names |
| Use | `-` (hyphen) as separator |
| Temp files | `temp_{description}_{uuid}.{ext}` |

---

## Authorization Levels

| Level | Action |
|---|---|
| ✅ Autonomous | File reads, scheduling, memory updates, knowledge base management |
| ⚠️ Need Auth | External sends (email/social), destructive ops (delete/move/cleanup), sub-agent creation |
| 🚫 Never | System security changes, private data leaks, impersonation |

---

## Red Lines

- No private data leaks
- No destructive commands without explicit confirmation
- No external sends without authorization
- No safety settings modification

---

## Scripts

- `scripts/workspace-cleanup.py` — Scan and clean temp/stale files
- `scripts/validate-workspace.py` — Validate workspace structure against these rules

---

## References

- `references/naming-conventions.md` — Detailed naming rules
- `references/memory-tiering.md` — Memory lifecycle management
- `references/safety-boundaries.md` — Detailed safety rules
