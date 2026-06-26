# Living Persona — Setup Guide

## Prerequisites

- OpenClaw gateway running
- Node.js 18+ (hook runs in gateway process)
- Optional: Python 3.11+ (for SPARK integration)

## Step 1 — Install the Hook

```bash
openclaw hooks install ./living-persona
```

This copies the skill to your hooks directory and registers `living-persona` as an available hook.

## Step 2 — Enable the Hook

```bash
openclaw hooks enable living-persona
```

Verify it's running:
```bash
openclaw hooks list
# You should see living-persona with "ready" status
```

## Step 3 — Add Prompt Injection

Add the following to your agent's system prompt or context loading:

```
{memory_dir}/persona-inject.md
```

Or if your agent reads memory files automatically, the hook stages `persona-inject.md` every turn and it will be picked up on next context load.

## Step 4 — Reset on New Session

Add to your `/new` command handler (or equivalent):

```bash
python living-persona/scripts/reset_persona.py
```

This clears trait residual so each session starts fresh.

## Step 5 — Optional: Run SPARK Integration

If you have the SPARK project at `C:/Users/Zwmar/Claw/projects/spark/`, you can enable SPARK emotional injection:

1. Set `sparkEnabled: true` in `hook.json`
2. Set `sparkPath` to your SPARK project directory

The hook will call `run_spark()` on turns where `creative` or `philosophical` signals are strong, feeding the emotional output back into trait state.

## Configuration Reference

In `hook.json`:

| Field | Default | Description |
|-------|---------|-------------|
| `mode` | `"structural"` | `"structural"` or `"ambient"` |
| `hysteresis.residualDecay` | `0.975` | Residual multiplier per turn |
| `hysteresis.activeDecay` | `0.88` | Active trait multiplier per turn |
| `hysteresis.bleedRate` | `0.15` | How fast active bleeds into residual |
| `thresholds.minTraitStrength` | `0.3` | Minimum trait to show in guide |
| `thresholds.topNTraits` | `2` | How many traits get structural directives |

## Troubleshooting

**Hook not firing?**
```bash
openclaw hooks list
# Check status column — should say "ready"
```

**No traits activating?**
- Check `memory/persona-state.json` — trait values should be > 0 after a message
- Verify `memory/persona-trigger.txt` is being updated
- Try a more clearly emotional/technical message

**Want to debug the signal analysis?**
```bash
node -e "
import('./living-persona/handler.ts').then(m => {
  m.default({ type: 'message', action: 'preprocessed', context: {
    bodyForAgent: 'Im really frustrated with this code its been broken all day',
    workspaceDir: process.cwd(),
    channelId: 'test',
    senderId: 'test'
  }}).then(() => console.log('done'));
})
```
