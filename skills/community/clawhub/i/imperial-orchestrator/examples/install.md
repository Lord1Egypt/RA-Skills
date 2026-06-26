# Install Examples

## Install into one workspace

```bash
mkdir -p ./skills
cp -R imperial-orchestrator-skill ./skills/imperial-orchestrator
```

## Install globally

```bash
mkdir -p ~/.openclaw/skills
cp -R imperial-orchestrator-skill ~/.openclaw/skills/imperial-orchestrator
```

## Preflight state

```bash
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/health_check.py \
  --openclaw-config ~/.openclaw/openclaw.json \
  --write-state ~/.openclaw/imperial_state.json
```
