# Release notes 0.2.0

## Summary

`openai-auth-switcher-public` 0.2.0 turns the public track from a script-first toolkit into a **web-first, install-first, onboarding-friendly release**.

This release focuses on:

- one-shot web preview installation
- generated admin credentials
- SSH-first access guidance
- first-run onboarding when `auth-profiles.json` is missing
- safer and more diagnosable `systemd --user` behavior

## Included in 0.2.0

- `install.sh` single-command shell entrypoint for end users
- `install_web_app.py` one-shot installer
- preferred port selection: `9527` → `12138` → random fallback
- generated web admin credentials and install summary
- local-only default bind (`127.0.0.1`)
- SSH tunnel command output
- onboarding-friendly web preview when auth is missing
- runtime/status summary for web service mode and readiness
- `systemd --user` preferred startup with background-process fallback
- improved reinstall behavior so changed unit env/port is actually applied
- stop helper that handles both systemd preview service and fallback pid-file mode

## Key fixes validated during 0.2.0 work

- fixed false display/runtime classification where systemd was active but UI/status still showed `background-process`
- fixed reinstall path where changed unit env/port did not reliably apply to the running preview service
- fixed stop/status mismatch where service had stopped but stale install-info still implied ready state
- reduced harmless first-install `reset-failed` noise by only running it when the preview unit already existed
- validated occupied-port fallback behavior for preferred ports

## Validation completed

Validated on the current Linux/OpenClaw environment:

- clean install → `systemd-user` ready
- install → stop → uninstall-like cleanup → reinstall
- `9527` occupied → fall back to `12138`
- `9527` + `12138` occupied → fall back to random free port
- stop helper disables/stops preview service cleanly
- status output reflects live systemd state instead of stale install-info alone

## Compatibility wording for publication

Recommended listing wording:

- Tested on OpenClaw `2026.3.11`
- Tested on Python `3.11`
- Tested on Node.js `22.x`
- Linux-first public release
- `systemd --user` preferred; background fallback retained

## Safety statement

This skill remains intended for administrators handling credential-adjacent OpenAI OAuth switching workflows.

The public release must still be packaged without live tokens, callbacks, backups, pid files, logs, or machine-specific runtime state.
