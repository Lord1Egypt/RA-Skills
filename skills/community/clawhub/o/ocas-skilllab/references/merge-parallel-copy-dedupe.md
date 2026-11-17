# Parallel-Copy Dedupe (Symlink Consolidation)

When to read: before collapsing a skill family that exists in multiple trees/profiles into one canonical copy.

### Parallel-copy dedupe (symlink consolidation)

When the SAME skill family exists in 3 places — a git monorepo tree (e.g. `eng-skills/engineering/`), a registry copy in an active profile (`$HERMES_HOME/../<p>/skills/...`), and/or a second profile (`koda`) — collapse to ONE canonical copy and symlink the rest. This is the dedupe half of "merge and dedupe."

**Step 0 — pick the canonical copy.** Normally the freshest (compare `git log` mtime or `find -printf '%T@'`). In the 2026-07-22 `engineering/` consolidation the repo's `engineering/` tree had the newest mtime and held in-progress edits, so it won; the old `eng-*` tree and the `Eng-*` registry copies were reconciled INTO it.

**Step 1 — BACK UP before any deletion.** Copy every source tree to a `_backup_<date>/` dir on disk (keep it out of git via `.gitignore`). Rollback if the superset check (Step 3) was wrong.

**Step 2 — merge unique files into canonical, by content not name.** For each source tree, walk files; for any file NOT present in canonical, `cp` it in. For files present in BOTH, keep the **newer** (`os.path.getmtime`). Byte-identical pairs need no action. Do NOT blindly overwrite — two trees may have DIVERGED in content, not just renamed (in that session, 29 `eng-*` vs `engineering/` files had the same name but different real content: renames + genuine edits). Overwriting canonical from source would clobber newer work.

**Step 3 — VERIFY superset before deleting.** Assert every file in every source tree now exists in canonical (same relative path). Script it (`os.walk` + set difference). If missing > 0, STOP — that is real data loss. Only after 0 missing do you remove the old trees.

**Step 4 — fix misnamed stragglers.** A copy may land under the wrong folder name with a wrong `name:`/`source:` (e.g. `engineering/eng-web-deployment/` carrying `name: util-web-deployment`). `mv` to the correct folder, rewrite `name:` + `source:` to match the canonical namespace.

**Step 5 — replace duplicate copies with symlinks.** After canonical holds everything, `rm -rf` each registry/profile copy and `ln -s <canonical-path> <copy-path>`. Symlink the whole parent dir where possible (e.g. `ln -s <fs-root>/eng-skills/engineering $HERMES_HOME/../koda/skills/software-development/engineering`) so each child skill resolves via the symlink. Verify: `test -e <symlink>/<skill>/SKILL.md` returns OK for every skill.

**Step 6 — commit + push the monorepo.** `git rm -r` the deleted trees (staged, reversible via `git restore --staged`), `git add -A`, commit, push. Untrack any `_backup_*/` (add to `.gitignore`) so the on-disk backup is NOT committed into the repo.

