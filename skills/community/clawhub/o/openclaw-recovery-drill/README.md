# OpenClaw Recovery Drill

**Backups are not the goal. Recoverability is.** This skill helps operators prove they can actually restore an OpenClaw deployment under pressure.

## What it does

`openclaw-recovery-drill` runs a lightweight readiness audit against an OpenClaw workspace and likely backup roots. It scores recovery posture, highlights missing recovery signals, and outputs a concrete drill plan.

Checks include:
- candidate backup root discovery
- presence of recent backup artifacts
- presence of core operator files in the workspace
- recovery/runbook signals
- backup freshness
- recommended next drill steps

## Install / Run

```bash
cd ~/.openclaw/workspace/skills/openclaw-recovery-drill
npm test
node scripts/recovery-drill.mjs --workspace ~/.openclaw/workspace
```

Optional explicit backup root:

```bash
node scripts/recovery-drill.mjs \
  --workspace ~/.openclaw/workspace \
  --backup-root ~/.openclaw/backups
```

## Output

The script prints JSON with:
- `score`
- `verdict`
- `summary`
- `findings`
- `recommendations`
- `drillPlan`
- `evidence`

Verdicts:
- `PASS` — looks usable for a lightweight drill
- `WARN` — partial coverage; recovery confidence is incomplete
- `FAIL` — restore confidence is too weak to trust

## Why this exists

Operators often mistake "backup files exist" for "we can recover." This skill is designed to push the conversation toward actual recovery readiness and drillable procedures.

## Package verification

```bash
npm test
npm pack --dry-run
```

## License

MIT
