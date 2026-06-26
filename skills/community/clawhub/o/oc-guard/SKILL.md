---
name: oc_guard
description: Safe OpenClaw config planning/apply workflow with bilingual execution receipts.
metadata: {"openclaw":{"requires":{"bins":["python3","openclaw","opencode"]}}}
---

# oc-guard Skill

## Purpose
All config-changing requests must go through `oc-guard`.
Do not directly edit `~/.openclaw/openclaw.json`.
When possible, invoke the bundled CLI at `{baseDir}/scripts/oc-guard.py`.

## Hard Rules
1. Use `oc-guard plan` before apply.
2. High-risk changes require `oc-guard apply --confirm`.
3. Always return execution receipt first.
4. If command is not executed, return `【模型说明-未执行】`.
5. Never claim success without a real `oc-guard` receipt.

## Common Commands
- `{baseDir}/scripts/oc-guard.py --help`
- `{baseDir}/scripts/oc-guard.py plan "<requirement>"`
- `{baseDir}/scripts/oc-guard.py apply --confirm "<requirement>"`
- `{baseDir}/scripts/oc-guard.py plan --proposal <file>`
- `{baseDir}/scripts/oc-guard.py apply --confirm --proposal <file>`
