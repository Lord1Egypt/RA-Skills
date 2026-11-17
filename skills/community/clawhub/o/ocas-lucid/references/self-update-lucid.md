# Lucid — Self-Update Procedure

`lucid.update` pulls the latest package from GitHub. Runs silently.

1. Read `source:` from frontmatter → extract `{owner}/{repo}`
2. Read local version from frontmatter `metadata.version`
3. Fetch remote version via `git fetch origin`
4. Check `git log HEAD..origin/main --oneline` for incoming commits
5. If no incoming commits → stop, already up to date
6. `cd {skill_dir} && git stash`
7. `git pull origin main` — **before pulling**, remove untracked files that would conflict with incoming tracked files (check `git status` for untracked files that match incoming additions):
   ```bash
   # Remove untracked files that conflict with tracked incoming files
   git checkout -- .
   # Or remove specific untracked files: rm -f references/foo.md references/bar.md
   ```
8. On pull failure → retry once, then report error
9. `git stash pop` — this may produce merge conflicts if stash modifies the same files the pull updated
10. On stash pop conflicts: **The stash ("theirs") is the local version; the pulled commit ("ours") is the remote.** Decide which version to keep:
    - If local version is newer (higher version number) → `git checkout --theighs <file>` to keep local
    - If remote version is newer → `git checkout --ours <file>` to keep remote
    - Resolve all conflicted files, then `git add -A && git commit -m "sync: merge remote update, keep vX.Y.Z"`
11. If stash was applied successfully, `git stash drop` to clean up
12. Output: `Updated Lucid from version {old} to {new}` with number of incoming commits

## Merge Conflict Quick Reference

When `git stash pop` produces conflict markers:
- `<<<<<<< Updated upstream` = the pulled remote commit
- `=======` = divider
- `>>>>>>> Stashed changes` = your local stash
- `git checkout --theirs <file>` = keep stash (local) version
- `git checkout --ours <file>` = keep pulled (remote) version
- After resolving: `git add <file>` (do NOT commit until all conflicts resolved)

## Known gotchas

- **Untracked files blocking merge**: If the stash tracked files that were previously untracked, the merge may abort with "untracked working tree files would be overwritten". Remove those untracked files first with `rm -f` or `git checkout -- .`.
- **read_file path resolution**: The `read_file` tool may fail with "File not found" for absolute profile paths (e.g., `<hermes-home>/skills/ocas-lucid/references/foo.md`). Use `read_file` with the expanded `~` path (`~/.hermes/profiles/indigo/skills/ocas-lucid/references/foo.md`) or fall back to `terminal(head <path>)`.
