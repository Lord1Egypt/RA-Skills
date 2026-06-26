---
name: joevault
description: Audit, classify, and quarantine stale paths after a profile switch, account migration, reset, or workspace move. Use when OpenClaw, Claude, WSL, Windows home directories, or project folders may still point at old locations, and when the user wants inactive state archived without breaking live paths.
---

# JoeVault

Archive old state without breaking live state.

## Quick start

1. Run `scripts/audit_paths.py` with the current root, stale root, and candidate relative paths.
2. Classify each stale path as `quarantine now`, `leave for inventory`, or `keep active`.
3. Quarantine only small, clearly inactive state first.
4. Inventory large stale workspaces before moving them.
5. When moving anything, use `scripts/quarantine_path.py` so the archive gets a manifest entry.

## Workflow

### 1. Audit first

Run the audit script before any move:

```bash
python3 scripts/audit_paths.py \
  --current-root /mnt/c/Users/Joseph \
  --stale-root /mnt/c/Users/Joe \
  --candidate .openclaw \
  --candidate openclaw-workspace \
  --search-root /mnt/c/Users/Joseph/.openclaw \
  --search-root /mnt/c/Users/Joseph/openclaw-workspace
```

What to look for:
- stale paths that still exist
- live configs that still reference stale paths
- symlinks that still point at old homes
- large directories that should not be moved blindly
- recent activity inside stale paths

### 2. Classify the stale paths

Use `references/classification.md` when deciding what to do.

Default rules:
- small old state directories like `.openclaw` or `.claude` are usually safe to quarantine first
- large workspaces, model folders, training outputs, or media trees must be inventoried before moving
- anything still referenced by live config is not ready for quarantine

### 3. Quarantine conservatively

Use quarantine for paths that are clearly inactive:

```bash
python3 scripts/quarantine_path.py \
  --source /mnt/c/Users/Joe/.openclaw \
  --archive-root /mnt/c/Users/Joseph/Archives/profile-switch-2026-03-31 \
  --label old-joe-openclaw
```

The script:
- creates the archive root if needed
- refuses to overwrite an existing target
- moves the source into the archive
- appends a manifest entry to `MANIFEST.md`

### 4. Inventory large trees before touching them

For large stale workspaces, get a top-level size view first:

```bash
du -sh /path/to/stale-workspace/* 2>/dev/null | sort -h | tail -n 30
```

Do not move a massive stale workspace until you know whether it contains:
- model weights
- voice assets
- training outputs
- media renders
- reference repos
- recent work

### 5. Verify the live system after every move

After any quarantine step, check:
- current symlinks still resolve correctly
- active configs no longer reference old paths
- the live service still starts
- the archive manifest records what moved and why

## Notes

- Prefer rename-and-quarantine over deletion.
- Prefer one small safe move over one giant risky move.
- If the user asks to “clean it all up,” still audit first.
- If a stale workspace had recent activity, treat it as a reference archive candidate, not trash.
