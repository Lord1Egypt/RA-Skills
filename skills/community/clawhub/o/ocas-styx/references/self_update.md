# Styx Self-Update Procedure

## When to run

- After a new version is pushed to the GitHub source
- When scripts or schema definitions need updating
- Periodic refresh (no fixed schedule — run on demand)

## Procedure

1. Pull the latest skill package from GitHub:
   ```bash
   cd {skill_root} && git pull origin main
   ```

2. Check for schema migrations in `references/schema.md`. If the schema version
   has changed, run the migration script:
   ```bash
   python3 {skill_root}/scripts/seed.py --migrate
   ```

3. Verify the database is intact:
   ```bash
   python3 -c "
   import sqlite3, os
   db = os.path.expanduser('~/.hermes/data/styx.db')
   conn = sqlite3.connect(db)
   tables = [r[0] for r in conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()]
   for t in tables:
       n = conn.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
       print(f'  {t}: {n} rows')
   conn.close()
   print('OK')
   "
   ```

4. Review `references/scripts.md` for any new or changed script flags.

## What updates do NOT touch

- `{agent_root}/data/styx.db` — enriched merchant data is never modified by updates
- `{agent_root}/data/transactions.db` — raw Plaid data is never modified by updates
- `{agent_root}/data/styx/review_queue.jsonl` — manual review queue is preserved
- `{agent_root}/data/banksync.md` — bank sync state is preserved

## Rollback

If an update causes issues:
```bash
cd {skill_root} && git reset --hard HEAD~1
```

## Gotchas

- **Untracked files block `git pull`** — `git stash` only stashes tracked files. Untracked files (new files not yet `git add`-ed) will block the merge. Move them aside before pulling:
  ```bash
  mv references/newfile.md /tmp/newfile.md.bak
  git pull origin main
  # then compare/restore if needed
  ```
- **`git stash pop` after a pull may produce merge conflicts** — especially if the pulled changes and the stashed changes touch the same lines. Resolve conflicts by editing the file, then `git add` and drop the stash.
- **`query.py --health-check` does not exist** — do not use it. Use the inline Python verification in step 3 above.