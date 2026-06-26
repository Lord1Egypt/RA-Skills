# essesseff Onboarding Utility

Automates essesseff app creation and Argo CD deployment setup using shell scripts.

## Overview

- **For subscribers**: Creates all 9 repos via the essesseff Public API (~5 minutes).
- **For non-subscribers** (`--non-essesseff-subscriber-mode`): Clones template repos, replaces strings, creates GitHub repos, and pushes (~1 minute).
- **Argo CD setup**: Configures Argo CD for dev, qa, staging, and/or prod environments.

## Setup

```bash
git clone https://github.com/essesseff/essesseff-onboarding-utility.git
cd essesseff-onboarding-utility
chmod +x essesseff-onboard.sh
# Optional wizard:
chmod +x essesseff-onboard-wizard.sh

cp essesseff-example.txt .essesseff
# Edit .essesseff with your values (or run essesseff-onboard-wizard.sh)
```

## Configuration Variables

### Required for essesseff Subscribers Only
- `ESSESSEFF_API_KEY` — API key from team account settings
- `ESSESSEFF_ACCOUNT_SLUG` — team account slug

### Required for All Operations
- `GITHUB_ORG` — target GitHub organization login
- `APP_NAME` — app name (lowercase letters, numbers, hyphens; no leading/trailing hyphens)

### For `--create-app`
- `TEMPLATE_NAME` — template name (e.g. `essesseff-hello-world-go-template`)
- `TEMPLATE_IS_GLOBAL` — `true` for global, `false` for account-specific

### For `--create-app` with `--non-essesseff-subscriber-mode`
- `GITHUB_ORG_ADMIN_PAT` — GitHub PAT with `repo` + `workflow` scopes (classic) or Contents/Metadata/Workflows R/W (fine-grained)

### For `--setup-argocd`
- `ARGOCD_MACHINE_USER` — Argo CD machine user username
- `GITHUB_TOKEN` — machine user PAT (`repo` + `read:packages`) — not the same as `GITHUB_ORG_ADMIN_PAT`
- `ARGOCD_MACHINE_EMAIL` — machine user email

### Optional
- `APP_DESCRIPTION` — app description
- `REPOSITORY_VISIBILITY` — `private` (default) or `public`
- `K8S_NAMESPACE` — override the destination K8s namespace (defaults to `GITHUB_ORG`; must be DNS compliant and < 63 characters)

### Optional — essesseff Subscribers Only
- `ARGOCD_INSTANCE_URL` — base URL of your Argo CD instance (e.g. `https://argocd.example.com`); when set, each environment's Argo CD app URL is registered with essesseff
- `ESSESSEFF_API_BASE_URL` — override essesseff API base URL (defaults to `https://essesseff.com/api/v1`)

## Commands

### List templates
```bash
./essesseff-onboard.sh --list-templates --config-file .essesseff
./essesseff-onboard.sh --list-templates --language go --config-file .essesseff
```

### Create app only
```bash
./essesseff-onboard.sh --create-app --config-file .essesseff
# Non-subscriber mode:
./essesseff-onboard.sh --create-app --non-essesseff-subscriber-mode --config-file .essesseff
```

### Create app + configure Argo CD
```bash
./essesseff-onboard.sh \
  --create-app \
  --setup-argocd dev,qa,staging,prod \
  --config-file .essesseff
```

### Configure Argo CD only (app already exists)
```bash
./essesseff-onboard.sh --setup-argocd dev,qa --config-file .essesseff
```

### Verbose / debug
```bash
./essesseff-onboard.sh --create-app --verbose --config-file .essesseff
```

## All CLI Flags

| Flag | Description |
|---|---|
| `--list-templates` | List available templates |
| `--language LANG` | Filter by language: go, python, node, java |
| `--create-app` | Create new essesseff app (all 9 repos) |
| `--setup-argocd ENVS` | Comma-separated environments: dev,qa,staging,prod |
| `--non-essesseff-subscriber-mode` | Clone/replace/push workflow, no API |
| `--config-file FILE` | Config file path (default: `.essesseff`) |
| `--verbose` | Enable debug output |
| `-h, --help` | Show help |

## How It Works

### App Creation
1. Validates app name (GitHub naming rules).
2. Checks app doesn't already exist.
3. Fetches template details.
4. Creates all 9 repos (API for subscribers; clone → replace → push for non-subscribers).

**String replacement (non-subscriber mode) — literal, case-sensitive:**
- `template_org_login` (e.g. `essesseff-hello-world-go-template`) → `GITHUB_ORG`
- `replacement_string` from template (e.g. `hello-world`) → `APP_NAME`

### Argo CD Setup
For each environment:
1. (Subscribers) Downloads `notifications-secret.yaml`.
2. Clones the argocd-env repo (`{app-name}-argocd-{env}`).
3. Creates `.env` file with required variables.
4. (Subscribers) Copies `notifications-secret.yaml` to repo.
5. Runs `setup-argocd.sh`.

**Variables written to `.env` files:**
- `ARGOCD_MACHINE_USER`, `GITHUB_TOKEN`, `ARGOCD_MACHINE_EMAIL`
- `GITHUB_ORG`, `APP_NAME`, `ENVIRONMENT`
- `K8S_NAMESPACE` (if set)

essesseff API credentials (`ESSESSEFF_API_KEY`, `ESSESSEFF_API_BASE_URL`, `ESSESSEFF_ACCOUNT_SLUG`) and app creation variables (`APP_DESCRIPTION`, `REPOSITORY_VISIBILITY`, `TEMPLATE_NAME`, `TEMPLATE_IS_GLOBAL`) are NOT copied to `.env` files as they are not needed by `setup-argocd.sh`.

## Troubleshooting

| Problem | Solution |
|---|---|
| `kubectl is not properly configured` | Configure kubectl for the target cluster — hard prerequisite |
| `App 'my-app' already exists` | Choose a different `APP_NAME` or delete the existing app |
| Template clone fails | Template repos are public. Check the git error (usually "Repository not found" or transient network issue). Retry. |
| Commit or push fails to argocd-env repo | Ensure `git config user.name` and `user.email` are set, and git profile has push access |
| Strings not replaced | Replacement is case-sensitive. Check `replacement_string` in `bundled-global-templates.json` matches what's in the template repo exactly. |
| K8s namespace rejected | `K8S_NAMESPACE` must be DNS compliant and < 63 chars. If unset, `GITHUB_ORG` is used — ensure it also meets these constraints. |
| Rate limit warning | Utility auto-retries. Wait for it. |

## Security

- Never commit `.essesseff` files — they contain secrets.
- `gitignore.txt` excludes `.essesseff` automatically (rename to `.gitignore` in your repo).
- Delete `notifications-secret.yaml` after applying it to your cluster.
