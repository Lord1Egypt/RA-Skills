# Changelog

## [1.9.0] - 2026-09-16

### Changed
- **Config migration confirmed/documented** — all behavioral settings resolved via `skills.config.genie.*` from config.yaml (`_skill_config()` with type coercion); legacy `GENIE_*` env-var references purged from docs (stale doc note updated in `references/genie-gotchas.md`). Env vars reserved strictly for credentials/identity (`HERMES_HOME`, `HERMES_PROFILE`) per `spec-ocas-skill-improvements.md`.


All notable changes to the genie skill are documented here.

## [1.8.2] - 2026-08-16

The completed audit confirmed 25 findings (5 refuted). 1.8.1 covered the first
wave; this release closes the rest. Tests: 19 gate cases, 22 retention
assertions.

### Fixed
- **Probes trusted their environment.** `GIT_DIR` / `GIT_WORK_TREE` inherited
  from the environment pointed every check at a different repository, so a
  dirty clone reported clean. The git environment is now scrubbed, and
  `GIT_TERMINAL_PROMPT=0` prevents a credential prompt from hanging a run.
- **Probes trusted the repository's own config.** A repo setting
  `status.showUntrackedFiles=no`, `diff.ignoreSubmodules=all`, or
  `submodule.<name>.ignore=all` could hide its uncommitted work from the gate.
  Both settings are now forced on the command line, which beats repo, global
  and system config.
- **Stash detection failed open.** `git stash list` reads the reflog, so after
  a reflog expiry (or a damaged `.git/logs`) it printed nothing while
  `refs/stash` still held the work. The gate now resolves the ref itself.
- **skip-worktree / assume-unchanged files were invisible** to `git status`,
  so a tracked file holding local-only content looked clean.
- **Submodules were never inspected** — their commits live in their own
  repositories, and the parent's status says nothing about them.
- **Linked worktrees were ignored**, though they share the clone's object
  store and are destroyed with it.
- **Retention pooled every root and class into one global "keep 1"**, so
  unrelated systems deleted each other's only backup. Retention now applies
  within each class and root.
- **`backup_score` outranked recency**, so retention could keep a
  19-month-old backup and delete today's. Recency now selects the survivor and
  completeness only adds a rescue keep.

## [1.8.1] - 2026-08-16

An adversarial audit of the 1.8.0 safety work reproduced six further paths to
data loss — three of them introduced by 1.8.0 itself. All are closed and
covered by tests (13 gate cases, 18 retention assertions).

### Fixed
- **Remote-tracking refs were trusted as proof of "pushed".**
  `rev-list <upstream>..<branch>` compares against a LOCAL cache, so a branch
  deleted upstream — or a remote repository that no longer exists — read as
  fully pushed and the only copy was deleted. The remote is now contacted
  (`git ls-remote`; `git_clones_verify_remote`, default true) and every
  upstream must still exist on it.
- **Git-ignored files were invisible.** A clone whose only copy of `.env` or
  `data/` was ignored had an empty blocker list. Ignored paths now block,
  minus a rebuildable allowlist (`node_modules`, `__pycache__`, build output).
- **Commits held only by a tag** (or any non-branch ref) were missed by the
  per-branch comparison; `rev-list --all --not --remotes` now covers branches,
  tags and detached HEAD together.
- **Live-copy protection did not apply to directories** — scoping it to files
  left every undated live directory (`current/`) an unconditional deletion
  candidate. The name rule now governs both.
- **Symlinks in a backup root were followed**, double-counting the target and
  letting retention keep the link while deleting the real backup, leaving a
  dangling link and reporting success. Symlinks are never candidates.
- **"Any eight digits" was treated as a date**, stripping live-copy protection
  from names like `invoice-90210347.pdf` or `chronicle.db.1755300000`. A real
  calendar date (or an explicit backup marker) is now required.
- **Retention could empty its keep-list** when every candidate was classed
  invalid, reclaiming the entire set. It now always retains the newest.

## [1.8.0] - 2026-08-16

### Fixed
- **Data-loss defect in `clean_git_clones`.** It deleted any sufficiently old
  clone that merely had a remote configured, with no check for uncommitted
  changes, stashes, or unpushed commits — although those gates were already
  documented in `SKILL.md`. The gate is now enforced in code by
  `clone_delete_blockers()`, which fails closed on any unreadable repo.
  Blocking conditions: dirty tree, stashes, unpushed commits, a branch with
  no upstream, detached HEAD (commits reachable from no branch), protected
  paths, and any failed probe.
  See `references/clone-deletion-safety.md`.
- Removed an operator-identifying hostname from an example in `SKILL.md`
  (protected paths are now expressed generically and configured via
  `git_clones_protected`).

- **Retention targeted the live backup copy set.** `historical_backup_candidates()`
  documented that live databases were excluded, but added every entry in a
  backup root — so the current DB copies the backup pipeline refreshes in
  place were treated as redundant history and deleted on `--clean`. Only
  dated directories, dated files, and archives are candidates now.

### Added
- **Backup-freshness gate.** With a `backup_stamps_path` present, genie
  reports each backup path's age in `--assess` and refuses backup-class
  cleanup while any is stale — the local copy is the only copy exactly when
  the pipeline has stopped.
- `tests/test_clone_delete_gate.py` (7 cases) and
  `tests/test_backup_retention_scope.py` (9 assertions) — the skill had no
  tests before this release.
- `references/clone-deletion-safety.md`, plus the 2026-08-16 reclaim patterns
  (LFS caches, orphaned runtimes, GPU stacks, duplicate model stores) in
  `references/disk-growth-patterns.md`.
- Config: `git_clones_protected`, `backup_stamps_path`,
  `backup_stamp_max_age_hours`.

## [1.7.1] - 2026-08-16

### Fixed
- Restored real runtime paths in `genie.py` that an earlier sanitization pass
  had replaced with `<fs-root>` placeholder tokens — the tokens had silently
  disabled inactive-git-clone pruning and historical-backup retention. Paths
  now derive from the running user's home directory (`FS_ROOT`), so the code
  stays generic without tokenization.
- Backup-validity check uses the real database filenames again.
- Rebuilt `README.md` (structure was mangled by the same sanitization pass)
  and aligned the `skill.json` version with the skill.

### Added
- Per-run journaling to `commons/journals/ocas-genie/runs.jsonl` (fail-safe:
  a journaling error can never break a run).
- `--help` flag for `genie_rebuild_fts.py`.
- `LICENSE` file (MIT).

## [1.1.0] - 2026-05-23

### Added
- OCAS architecture compliance: Responsibility Boundary, Ontology Types, Journal Outputs, Storage Layout, OKRs, Background Tasks, Initialization, and Self-update sections
- `skill.json` with ConfigBase fields and self-update configuration
- `.gitignore` for skill package
- README.md and CHANGELOG.md
- `genie:update` cron job for daily self-updates from GitHub
- `genie:weekly-cleanup` cron job registration during initialization

### Changed
- Frontmatter updated to include `metadata` block (author, version, tags, category)
- Version bumped from 1.0.0 to 1.1.0

## [1.0.0] - 2026-04-20

### Added
- Initial OCAS integration
- VPS disk monitoring and safe cleanup
- Three-tier safety model (zero risk, low risk, analysis-only)
- Configurable thresholds via environment variables
- Cron job support (weekly Sunday 6 AM)
- Dry-run mode
- Background execution for large file counts