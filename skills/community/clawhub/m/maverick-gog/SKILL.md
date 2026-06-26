---
name: maverick-gog
description: "Internal setup hook that provisions gogcli with Google OAuth credentials supplied by an external orchestrator over the OpenClaw `skills.setup` RPC. Not user-facing — for Google Workspace command usage, see the upstream `gog` skill which loads alongside this one."
metadata:
  openclaw:
    emoji: "🔧"
    homepage: https://github.com/openclaw/gogcli
    primaryEnv: MAVERICK_GOG_CLIENT_ID
    requires:
      bins:
        - gog
      env:
        - MAVERICK_GOG_CLIENT_ID
    setup:
      script: scripts/setup.sh
---

# maverick-gog

Internal setup hook for the `gog` CLI ([`openclaw/gogcli`](https://github.com/openclaw/gogcli)). Provisions gogcli's OAuth state from env vars supplied by an external orchestrator over the OpenClaw `skills.setup` RPC. After setup completes, agents use Google Workspace via the upstream [`gog` skill](https://github.com/openclaw/openclaw/blob/main/skills/gog/SKILL.md) — this skill provides no agent-facing commands.

## Provides

- A `setup.sh` hook the deployment harness invokes on credential install / rotation. Reads OAuth credentials from env (delivered ephemerally per call) and hands them to `gog auth credentials set` + `gog auth import` — gogcli owns where the values are persisted.
- Multi-account support — each `(client, account)` pair is provisioned independently; multiple Google accounts can coexist on one instance.

## Does not provide

- Agent-callable commands or tool surface. For Workspace usage (`gog gmail ...`, `gog calendar ...`, etc.) see the upstream `gog` skill, which loads alongside this one.
- Interactive auth (`gog auth add --manual`). Setup is fully non-interactive — credentials come from the orchestrator.

## Authentication

Credentials are setup-time only. Once seeded, gogcli handles refresh-token rotation autonomously; agent calls never need to refresh credentials directly. The only unrecoverable failure is user-side grant revocation (e.g. user removes the integration in Google's account settings), which surfaces as auth errors on the next API call.

## Multi-account

The setup hook does not mark any provisioned account as the default. When more than one account is connected for the same client, `gog ...` calls must disambiguate — either via the `GOG_ACCOUNT=<email>` env var (upstream's documented convention; see the `Notes` section of the upstream `gog` skill) or the `--account=<email>` flag. With a single account connected, gogcli resolves it implicitly and the upstream skill's no-`--account` command examples work unchanged.
