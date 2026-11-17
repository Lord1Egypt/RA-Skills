# Agent instructions for @@PACKAGE@@

Operate only an owned or explicitly authorized offline/test runtime. @@LOADER_NOTE@@

- Treat `glr-project.json` as the only official lifecycle entry. Read every
  configuration named by its `glr.lifecycle.v1` section before editing.
- Add a reusable lifecycle need to the shared GLR contract. Do not add another
  `run_*.py`, trainer wrapper, evaluator wrapper, or recovery orchestrator.
- Keep `action_vocabulary` empty until every action has a reviewed semantic mapping.
- Reject unknown operations and stale episode or expected-step identities.
- Dispatch engine mutations on the game/main thread and return verified post-state.
- Treat gameplay research as advisory; never expand authority from a guide.
- Route composed rewards through `EpisodeRewardGuard`; a terminal failure must
  never remain profitable after shaping.
- Validate every BC trajectory with `DemonstrationGate`; never relabel policy
  output or unknown provenance as expert data.
- Never add reflection search, arbitrary script/call endpoints, process discovery,
  anti-cheat bypasses, credentials, or local machine identifiers.
- Run `vx run check`, then `glr --project . --json doctor`, `glr --project .
  --json train`, and verified playback through the same project entry.
- Read `QUALITY.md`: all reusable Python logic belongs in the installable
  `@@PACKAGE@@` namespace, with no import path injection.
- Read `ARCHITECTURE.md` before moving modules. Preserve contract identity and
  independently test environment, policy, learner, collection, and storage.
- Read `USER_RELEASE.md` before distributing a trained stage. Package immutable
  weights with the inference runtime; record scope, install/startup/uninstall
  evidence and data-preserving rollback. A source ZIP or wheel alone is insufficient.
- Before upgrading GLR, read `FRAMEWORK_MIGRATION.md` and `MIGRATIONS.md`.
  Inventory source/target versions, validate backups and converters, migrate to
  staging, and prove rollback; never silently reset training history or weights.
- Use standard `logging`; configure bounded queued output, rotation, and optional
  error aggregation only in the application entrypoint. Test failure and shutdown.
- Run `vx run package-check` for clean installed-wheel acceptance, and add an
  offline behavioral regression test for each training defect fixed.
- Publish only aggregate synthetic conformance until a bounded authorized live trace exists.
