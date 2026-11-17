# Framework migrations for @@PACKAGE@@

The scaffold has not performed any framework or persistent-data migration.
Follow `FRAMEWORK_MIGRATION.md` for each upgrade and add a record below.
Keep credentials, account IDs, and private backup paths out of public reports.

## Upgrade record template

- Status: planned / dry-run-verified / cutover-verified / rolled-back / blocked
- Source: GLR/application/Python/CLI/host/provider versions, revision, lock digest
- Target: explicit versions, release-note references, compatibility constraints
- Compatibility: Python APIs / configuration / run store / datasets / checkpoints
- Baseline: offline test commands and results; pre-existing failures
- Backup: private receipt reference, consistency method, checksum, restore result
- Converter: package/module, revision, accepted schemas, dry-run command
- Staging: output reference, interruption and repeat-execution behavior
- Validation: counts, IDs, lineage, hashes, replay, checkpoint/resume invariants
- Code acceptance: static/unit/contract/wheel/training/logging results
- Cutover: writer coordination, switch/readback, authorized live acceptance
- Rollback: triggers, verified commands, post-cutover write handling
- Losses and limitations: transformations, warm starts, deferred gates

Record actual evidence; an empty checklist is not acceptance.
