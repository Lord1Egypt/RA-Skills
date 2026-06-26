# Night Shift Install and Setup

## Install from ClawHub

```bash
openclaw skills install vardhineediganesh877-ui/night-shift
```

## Verify local requirements

```bash
cd ~/.openclaw/workspace
python3 skills/night-shift/scripts/preflight.py --json
```

Required dependencies are `python3` and `git`. Cursor/Claude runners are optional, but any queued phase that uses them requires those CLIs to work non-interactively.

## Recommended first run: disposable workspace

```bash
export OPENCLAW_WORKSPACE=/tmp/night-shift-demo
mkdir -p "$OPENCLAW_WORKSPACE"
python3 ~/.openclaw/workspace/skills/night-shift/scripts/preflight.py --json
python3 ~/.openclaw/workspace/skills/night-shift/scripts/executor.py dry-run
```

Dry-run should write a preview report only. It should not mark plans complete or create success checkpoints.

## Background/systemd setup

Detached timers need explicit environment. Create a private env file if needed:

```bash
cp skills/night-shift/.night-shift.env.example ~/.openclaw/workspace/.night-shift.env
chmod 600 ~/.openclaw/workspace/.night-shift.env
```

Then edit values for your environment. Do not commit real secrets.

Before enabling a timer, run preflight in the same user context that will run the service.
