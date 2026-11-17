---
name: "mochi-claw-maintenance"
description: "Inspect one selected OpenClaw instance and its agent bindings, create verified private snapshots, compare changes and rehearse restoration in a new directory. Use for OpenClaw Maintenance and Migration Desk."
metadata: {"openclaw": {"requires": {"anyBins": ["python3", "python"]}, "homepage": "https://mochilab.bz", "version": "1.0.2"}}
---

# OpenClaw Maintenance and Migration Desk

## Select exactly one instance

Use this skill for an owner/operator's local OpenClaw inventory, snapshots, integrity checks, change comparison and restore rehearsal. Read [references/input.md](references/input.md). Resolve the intended OpenClaw state directory with the user; do not scan unrelated home directories, other instances or other projects. This first release provides read-only CLI status, verified snapshots and rehearsals. Updates, live restores, service restarts, pairing approvals and chat tests remain separate operations in the installed native CLI, performed only when specifically requested.

Use Python 3.10+ with the standard library. Choose a dedicated maintenance workspace OUTSIDE the selected instance root so snapshots cannot recursively include themselves. Create this private output location as part of the requested backup operation; keep it separate from existing agent workspaces.

```text
python3 "{baseDir}/scripts/run.py" --workspace "/home/ubuntu/openclaw-maintenance" --instance-root "/home/ubuntu/.openclaw" --input "request.json"
```

inspect reads strict JSON configuration and reports agent IDs, workspace paths, bindings and conflicting/undeclared routes. It accepts current agents.entries dictionaries and legacy agents.list arrays. It redacts credential fields in its separate config report. For JSON5, use the host's native config tooling or an explicitly created normalized copy; do not rewrite live config just to satisfy the parser. cli-status calls only --version, gateway status --json and agents list --json with explicit state/config paths. Non-JSON CLI output is suppressed, not presented as verified health.

## Snapshot and verification

The default snapshot includes openclaw.json, agents, credentials, identity and workspace/workspace-* folders directly inside the selected root. It retains installed Skills and .mochilab Skill state; node_modules, .git, __pycache__, lock and SQLite WAL/SHM sidecars are excluded. An explicit include list is root-relative and must retain openclaw.json. Links and external paths are rejected. Review omittedExternalWorkspaces in backup-receipt.json: workspaces outside this root need their own explicit backup before a complete migration.

A snapshot contains credentials. For a user-requested private backup, set sensitiveBackupAccepted:true and keep the archive private. Non-SQLite files are hashed before and after the whole capture; detected changes fail the run. SQLite files use the SQLite online backup API and an integrity check, not a raw copy of an active DB. For a consistent point in time across multiple stores, quiesce writes first through the actual service owner. Mode 600 is used on files; on Windows use a user-private directory with suitable inherited ACLs.

verify rejects traversal, duplicate/case-colliding paths, links, extra/missing files and mismatched size/hash receipts. rehearse restores only into a NEW export directory and rechecks every file. It does not start a Gateway or activate restored credentials. compare lists added/changed/removed paths; DB byte changes are not a semantic data diff.

Deliver inventory, verified ZIP and rehearsal/compare receipts as requested. A successful rehearsal proves file recovery, not live service behavior. For a real migration, use the installed version's help for update/backup/restore, preserve agent/account routing, then test the actual model and chat account. Do not invent a successful chat reply or replace one account's binding with another's.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
