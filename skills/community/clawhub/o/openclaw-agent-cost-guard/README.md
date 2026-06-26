# OpenClaw Cost Guard

**Cheap tokens are only useful if agent spend stays intentional.** This skill helps detect lightweight denial-of-wallet risks in an OpenClaw config before they scale.

## What it does

`openclaw-cost-guard` performs a static review of an OpenClaw config and looks for obvious cost-risk signals.

Checks include:
- missing explicit budget fields
- premium-model signals in routine defaults
- oversized token ceilings
- browser / interactive workflow cost hints
- recurring automation without obvious budget guardrails
- verbose / thinking signals that may add routine spend

## Install / Run

```bash
cd ~/.openclaw/workspace/skills/openclaw-cost-guard
npm test
node scripts/cost-guard.mjs --config ~/.openclaw/openclaw.json
```

If `--config` is omitted, the script checks the default OpenClaw config path.

## Output

The script prints JSON with:
- `score`
- `verdict`
- `summary`
- `findings`
- `recommendations`
- `guardrails`
- `evidence`

Verdicts:
- `PASS` — no major lightweight governance gap found
- `WARN` — spend risk exists and should be reviewed
- `FAIL` — denial-of-wallet risk is materially elevated

## Why this exists

OpenClaw makes it easy to wire together powerful agents, cron jobs, browser workflows, and premium models. That also makes it easy to create silent recurring spend. This skill exists to surface those risks early.

## Package verification

```bash
npm test
npm pack --dry-run
```

## License

MIT
