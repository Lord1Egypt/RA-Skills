# Upgrade & Runtime Re-Sync Contract

ClawHub updates the packaged skill tree under `skills/openclaw-memory-canonical/`.
It does **not** automatically overwrite deployed runtime scripts under `memory/scripts/`.

## Required after install/update

Run from the workspace root:

```bash
mkdir -p memory/scripts
cp skills/openclaw-memory-canonical/scripts/*.sh memory/scripts/
chmod +x memory/scripts/*.sh
bash memory/scripts/health-check.sh
```

## Why this is required

The packaged skill is the reference artifact.
The deployed runtime is whatever currently exists in `memory/scripts/`.
If you update the skill package but skip the re-sync step, runtime behavior may still reflect older deployed scripts.

## Optional drift check before overwrite

If you maintain local script variants (for example `memory/scripts/*.local.sh` wrappers or custom instrumentation around `memory/scripts/health-check.sh`, `memory/scripts/atomic-write.sh`, `memory/scripts/archive-old-episodic.sh`, or `memory/scripts/archive-old-learnings.sh`), back them up before overwriting deployed runtime scripts.

```bash
mkdir -p memory/scripts-backup
cp -a memory/scripts/*.local.sh memory/scripts-backup/ 2>/dev/null || true
cp -a memory/scripts/health-check.sh memory/scripts/atomic-write.sh memory/scripts/archive-old-episodic.sh memory/scripts/archive-old-learnings.sh memory/scripts-backup/ 2>/dev/null || true

diff -u skills/openclaw-memory-canonical/scripts/health-check.sh memory/scripts/health-check.sh || true
diff -u skills/openclaw-memory-canonical/scripts/atomic-write.sh memory/scripts/atomic-write.sh || true
diff -u skills/openclaw-memory-canonical/scripts/archive-old-episodic.sh memory/scripts/archive-old-episodic.sh || true
diff -u skills/openclaw-memory-canonical/scripts/archive-old-learnings.sh memory/scripts/archive-old-learnings.sh || true
```

## Deterministic restore snippet

If you need to restore the backed-up deployed scripts after a failed overwrite test:

```bash
cp -a memory/scripts-backup/health-check.sh memory/scripts-backup/atomic-write.sh memory/scripts-backup/archive-old-episodic.sh memory/scripts-backup/archive-old-learnings.sh memory/scripts/ 2>/dev/null || true
cp -a memory/scripts-backup/*.local.sh memory/scripts/ 2>/dev/null || true
bash memory/scripts/health-check.sh
```

## Release trust rule

Do not claim that a newly installed or updated package changed runtime behavior until:
1. the relevant scripts were re-synced into `memory/scripts/`, and
2. `bash memory/scripts/health-check.sh` passed afterward.
