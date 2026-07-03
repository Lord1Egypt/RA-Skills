---
name: infisical-reader
description: "Direct REST API reader for Infisical secrets. Lightweight, no middleware. Use when the agent needs to fetch API keys or credentials from Infisical."
---

# Infisical

Read secrets from [Infisical](https://infisical.com) via REST API.

## User Setup

1. Create Machine Identity: Organization → Access Control → Machine Identities.
2. Add Universal Auth to the identity → save Client ID + Client Secret.
3. Grant identity access to each project: Project Settings → Access Control → Identities → add as Member.
4. Store credentials in `~/.openclaw/.env`:

```
INFISICAL_CLIENT_ID=<client-id>
INFISICAL_CLIENT_SECRET=***
```

## Agent Workflow

1. `POST /api/v1/auth/universal-auth/login` → `{"clientId":"...","clientSecret":"***"}` → `accessToken`
2. `GET /api/v1/workspace` → list projects (id, slug, environments)
3. `GET /api/v3/secrets/raw?workspaceId=<id>&environment=<env>&secretPath=/` → secrets

## Script

```bash
# List projects
python3 {baseDir}/scripts/infisical.py --list-projects

# Read all secrets
python3 {baseDir}/scripts/infisical.py -w <workspaceId> -e prod

# Get single secret (raw value)
python3 {baseDir}/scripts/infisical.py -w <wid> -e prod -k OPENAI_API_KEY --raw
```

Requires `INFISICAL_CLIENT_ID` and `INFISICAL_CLIENT_SECRET` in `~/.openclaw/.env`.

## Notes

- Use `workspaceId` (not `projectSlug`) — slug may not work in all API versions.
- Tokens are short-lived; re-authenticate each session.
- Too many failed logins temporarily locks Universal Auth.
- Free tier: up to 5 Machine Identities.
- Detailed API reference: see `{baseDir}/references/api.md`
