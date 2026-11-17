# Skill Script Placement Convention

## The Rule

**If a script's filename contains a skill's name, it belongs inside that skill's `scripts/` directory.**

## Exceptions

Infrastructure scripts with no single parent skill stay in `~/.hermes/scripts/`:
- `google_auth.py` — shared OAuth helper (imported by dispatch, taste, bower)
- `ladybug_client.py` — shared DB client (imported by elephas)
- `update_<skill>.sh` — skill update entry points (cron compatibility)

## Cron Compatibility Pattern

Cron requires scripts at relative paths in `~/.hermes/scripts/`. Use **direct symlinks** (not wrappers):

```
ln -s <skill>/scripts/<name> ~/.hermes/scripts/<name>
```

**Do NOT use wrapper scripts** (a `.sh` that `exec`s the real script). Direct symlinks work fine — the cron path validator only rejects symlinks during `cronjob update` API calls, not at execution time.

## Update Script Pattern

`~/.hermes/scripts/update_<skill>.sh` → `skills/<skill>/scripts/update.sh`

The canonical copy lives in the skill dir. The symlink is for cron compatibility only.

For skills without a `scripts/` dir, create the `update_<skill>.sh` as a regular file in `~/.hermes/scripts/`.

## Symlink Chain Pitfall

Avoid circular symlink chains like:
```
skill_update.py ocas-* → update_*.sh → skill_update.py ocas-*
```

Instead, `update_*.sh` should directly call the update mechanism, and `skill_update.py ocas-*` symlinks should point to `update_*.sh`.

## Dead Code Sweep

After moving scripts into skills, sweep `~/.hermes/scripts/` for files no longer imported or referenced:
- Check imports: `grep -rl "from <name>\|import <name>" skills/*/scripts/*.py`
- Check broken symlinks: `find ~/.hermes/scripts -type l ! -e`
- Delete anything with 0 active references

## One-Time Scripts Get Deleted

One-time fix scripts and test scripts should be deleted after use, not archived. If it has "fix_" or "test_" in the name and isn't in a skill, delete it.