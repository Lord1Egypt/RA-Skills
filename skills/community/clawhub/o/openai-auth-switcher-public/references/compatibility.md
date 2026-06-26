# Compatibility

## Release intent

This skill is the **public/publishable track** of the OpenAI auth switcher workflow.

It is designed for redistribution through ClawHub as an AgentSkill package and therefore prefers:

- explicit compatibility statements
- portable path detection
- sanitized packaging
- conservative defaults

## Tested baseline

Current baseline used during initial public-skill design:

- OpenClaw: `2026.3.11`
- Python: `3.11`
- Node.js: `22.x`
- OS: Linux

## Recommended compatibility statement for first public release

Until broader validation is completed, publish with wording similar to:

- **Tested on OpenClaw 2026.3.11**
- **Tested on Python 3.11**
- **Tested on Node.js 22**
- **Linux-only for the first public release**

## Minimum version policy

Do not claim a minimum OpenClaw version lower than the lowest version actually validated with real runtime checks.

Suggested first-release policy:

- Prefer `Tested on` wording first
- Add `Requires >=` only after explicit compatibility verification

## Python expectations

Public scripts should target Python `>= 3.10` unless a feature strictly requires newer syntax.

If later scripts use `tomllib` or other version-sensitive modules, update this file and `doctor.py` together.

## Node expectations

If the public skill includes optional web or OAuth helper scripts, document Node separately as:

- optional for runtime inspection-only usage
- required for specific web/OAuth flows

## OS expectations

First public release scope:

- Linux only
- systemd user-service support is optional, not mandatory

## Analytics capability note

The public track can include local token attribution and hourly/daily rollup scripts, but these are explicitly documented as:

- local estimation only
- dependent on locally available session usage data
- not official provider billing

## Out of scope for the first public release

- Windows support (not officially validated in `0.1.0`)
- macOS support (not officially validated in `0.1.0`)
- guaranteed compatibility with custom/private OpenClaw forks
- guarantees for machine-specific pnpm-store paths
- bundling live OAuth session artifacts
