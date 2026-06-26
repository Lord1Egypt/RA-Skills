# Install and runbook

## First-run sequence

1. Install the skill.
2. Run the compatibility doctor.
3. Review runtime discovery output.
4. Only then run inspection or switching workflows.

## Recommended first commands

For local testing of the public track, prefer an external state directory so the source tree stays clean:

```bash
export OPENAI_AUTH_SWITCHER_PUBLIC_STATE_DIR=/tmp/openai-auth-switcher-public-runtime
bash ~/.openclaw/workspace/skills/openai-auth-switcher-public/install.sh
```

If install fails and you need diagnostics:

```bash
python3 skills/openai-auth-switcher-public/scripts/doctor.py --json
python3 skills/openai-auth-switcher-public/scripts/env_detect.py --json
python3 skills/openai-auth-switcher-public/scripts/inspect_runtime.py --json --include-status --include-sessions
```

## Slot management now available in the public track

```bash
python3 skills/openai-auth-switcher-public/scripts/profile_slot.py create --slot account-a --display-name "主号A"
python3 skills/openai-auth-switcher-public/scripts/profile_slot.py list
python3 skills/openai-auth-switcher-public/scripts/profile_slot.py show --slot account-a
```

## Controlled switch experiment now available in the public track

Dry-run first:

```bash
python3 skills/openai-auth-switcher-public/scripts/switch_experiment.py --target-slot account-a --dry-run --json
```

Then, only if the target profile is correct, run the actual switch experiment.

## Web preview control helpers

```bash
python3 skills/openai-auth-switcher-public/scripts/status_web_app.py
python3 skills/openai-auth-switcher-public/scripts/restart_web_app.py
python3 skills/openai-auth-switcher-public/scripts/stop_web_app.py
bash ~/.openclaw/workspace/skills/openai-auth-switcher-public/uninstall.sh
```

Notes:
- `stop_web_app.py` now stops both the `systemd --user` preview service and any fallback background PID file process.
- `uninstall.sh` is the recommended cleanup entrypoint before `clawhub uninstall`; it stops the preview service, removes the local systemd unit, and clears temporary runtime files under `skill-data/runtime`.
- `install_web_app.py` only runs `systemctl --user reset-failed` when the preview unit already exists, to avoid harmless first-install noise.
- Temporary runtime files can live inside the skill runtime area, but important persistent state should be moved outside the skill tree with `OPENAI_AUTH_SWITCHER_PUBLIC_STATE_DIR` to avoid accidental loss during uninstall or upgrade.

## Rollback helper now available in the public track

```bash
python3 skills/openai-auth-switcher-public/scripts/rollback_experiment.py --backup-file /path/to/auth-profiles.json.bak.xxx --json
```

## What doctor should confirm

- Python version is supported
- Node version is present if optional web flows are requested
- OpenClaw root can be discovered or is explicitly configured
- auth runtime files exist
- no live secret-bearing runtime data is being packaged for publication

## Safe publication workflow

Use this skill directory as the publication source.

```bash
python3 skills/openai-auth-switcher-public/scripts/package_public_skill.py
```

Then publish the generated `.skill` artifact or publish the public skill folder with ClawHub after verifying package contents.

See also:

- `references/release-notes-0.1.0.md`
- `references/publish-checklist.md`
- `references/publish-command-example.md`

## Operational split

Keep two tracks:

- internal/live operator track: `skills/openai-auth-switcher`
- public/release track: `skills/openai-auth-switcher-public`

Do not merge runtime state back from the internal track into the public track.
