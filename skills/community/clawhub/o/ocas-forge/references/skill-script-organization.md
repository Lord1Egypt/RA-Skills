# Skill Script Organization Convention

## Rule: Scripts belong in their skill

If a script has a skill name in it (e.g., `taste_cleanup.py`, `plaid_sync.py`), it belongs in that skill's `scripts/` directory.

## Standard layout

```
skills/<name>/
  SKILL.md
  references/
  scripts/          ← all executable scripts for this skill
    update.sh       ← self-update script (always named update.sh)
    ...
```

## Cron compatibility

The cron system requires script paths relative to `~/.hermes/scripts/`. Use **symlinks** (not wrappers):

```
ln -s <hermes-home>/skills/<name>/scripts/<script> <hermes-home>/scripts/<script>
```

The canonical copy lives in the skill dir. The symlink in `~/.hermes/scripts/` is for cron compatibility.

**Do NOT create wrapper scripts** that `exec` the real script. Use direct symlinks. The cron path validator may reject symlinks during `cronjob update` API calls, but they work fine at execution time.

## Symlink chain pitfall

Avoid circular chains: `skill_update.py ocas-*` → `update_*.sh` → `skill_update.py ocas-*`.

Correct flow: `update_*.sh` calls `skill_update.py ocas-*` directly. `skill_update.py ocas-*` symlinks point to `update_*.sh`.

## Infrastructure scripts stay in ~/.hermes/scripts/

Cross-cutting infrastructure with no single parent skill:

| File | Purpose | Imported by |
|------|---------|-------------|
| `google_auth.py` | Shared OAuth helper | dispatch, taste, bower (9 scripts) |
| `ladybug_client.py` | Shared DB client | elephas (2 scripts) |
| `update_<skill>.sh` | Skill update entry points | cron jobs |

## Dead code patterns

These files were deleted from `~/.hermes/scripts/` — do not recreate:
- `oauth_helper.py` — replaced by `google_auth.py` (in `scripts/`)
- `mcp_query.py` — unused
- `skill_update.py` — replaced by the git-based update flow
- `ladybug_bridge.py` — unused
- `fix-*.py`, `post_update_*.sh` — one-time scripts, deleted after use

## Update script pattern

Each skill's self-update is `scripts/update.sh`:
- For GitHub-backed skills: does `git reset --hard && git pull`
- For git-less skills: may use `self_update.py` or custom logic
- Symlinked from `~/.hermes/scripts/update_<skill>.sh` for cron