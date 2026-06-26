# Auth

## Install

Published CLI package:

```bash
npm i -g @mibatt/dietu@latest
```

Local repo development:

```bash
cd cli
npm install
npm link
dietu --help
```

## Human interactive login

Preferred command:

```bash
dietu auth login
```

Behavior:

- CLI starts GitHub device flow
- Terminal shows `verification_uri` and `user_code`
- Browser may open automatically
- If browser does not open, manually visit the shown URL and enter the code
- On success, CLI stores the short-lived session token in the local profile

Check status:

```bash
dietu auth status
```

Clear local profile token:

```bash
dietu auth logout
```

## Automation and PAT

Recommended path:

- Create a PAT in Dietu web `Settings / Access Tokens`
- Put that PAT into `DIETU_ACCESS_TOKEN`

Examples:

```bash
DIETU_ACCESS_TOKEN=dt_pat_xxx dietu auth status
DIETU_ACCESS_TOKEN=dt_pat_xxx dietu market overview --format json
dietu market overview --token "$DIETU_ACCESS_TOKEN" --format json
```

Guidance:

- PAT is the recommended long-lived credential for CI, agents, scripts, and servers
- JWT from `dietu auth login` is a short-lived session credential
- If `auth status` returns `token_mode: bearer_pat`, the CLI is using a PAT
- If it returns `token_mode: bearer_jwt`, the CLI is using a session JWT

## Base URL and profiles

**Default API**: `https://dietu-api.mibatt.com`

Common flags:

```bash
dietu auth login --base-url http://localhost:5001  # 本地开发
dietu auth status --profile prod                  # 使用 prod profile
```

Environment variables:

- `DIETU_BASE_URL`
- `DIETU_PROFILE`
- `DIETU_OUTPUT`
- `DIETU_ACCESS_TOKEN`
- `DIETU_CONFIG_DIR`

Resolution order:

1. Command line flags
2. Environment variables
3. Profile config
4. Defaults

## Legacy fallback

Compatibility-only password login still exists:

```bash
dietu auth login --email you@example.com --password '***'
```

Use it only when the environment cannot complete device flow.
