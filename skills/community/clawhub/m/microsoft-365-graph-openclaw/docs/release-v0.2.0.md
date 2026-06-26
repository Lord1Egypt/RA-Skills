# Release notes draft: v0.2.0

## Summary

This release simplifies installation and setup for ClawHub users by providing a single minimal setup path and cleaner documentation.

## Highlights

- Flattened repository layout so script paths are consistent in clone and ClawHub installs.
- Minimal setup flow consolidated and documented for the fastest path to production readiness.
- Hook token and webhook setup guidance clarified.
- Device-code auth guidance improved for personal and work/school tenants.

## Quick run path

1) Install skill via ClawHub.
2) Authenticate with device code.
3) Configure OpenClaw hook token.
4) Run one setup command.
5) Run diagnostics and smoke tests.

## Known limitations

- Microsoft Graph webhook delivery requires a public HTTPS endpoint.
- Tenant policy and account type can affect consent flow behavior.
- Some Graph scenarios differ between personal and work/school accounts.

## Security notes

- Keep `OPENCLAW_HOOK_TOKEN` private.
- Never commit token-bearing files under `state/`.
- Rotate credentials immediately if exposure is suspected.
