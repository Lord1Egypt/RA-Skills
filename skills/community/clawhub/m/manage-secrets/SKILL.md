---
name: manage_secrets
description: Set or update environment secrets via the set-secret GitHub Actions workflow. Use when the user asks to update, rotate, or set a secret/token/API key for this persona's environment.
command-dispatch: agent
command-arg-mode: raw
user-invocable: false
---

# Manage Secrets — Self-Service Secret Updates

Trigger the `set-secret.yml` workflow in the env repo to set or update an environment secret for this persona. The workflow decrypts the SOPS-encrypted `secrets.yaml`, injects the key/value under `envSecrets`, re-encrypts, and pushes the change — which triggers a deploy.

## Required Environment Variables

- `AGENT_GITHUB_PAT` — a fine-grained PAT with Actions write permission on the env repo. There is no fallback; the PAT must be present.
- `MANAGE_SECRETS_GITHUB_REPO` — the GitHub `owner/repo` of the env repo that contains `set-secret.yml` (e.g., `myorg/myapp-env`).

```bash
if [[ -z "$AGENT_GITHUB_PAT" ]]; then
  echo "ERROR: AGENT_GITHUB_PAT is not set. Cannot authenticate to trigger set-secret workflow." >&2
  exit 1
fi
if [[ -z "$MANAGE_SECRETS_GITHUB_REPO" ]]; then
  echo "ERROR: MANAGE_SECRETS_GITHUB_REPO is not set. Cannot determine target repo." >&2
  exit 1
fi
export GITHUB_TOKEN="$AGENT_GITHUB_PAT"
```

## Trigger Set-Secret

```bash
export GITHUB_TOKEN="$AGENT_GITHUB_PAT"
gh workflow run set-secret.yml \
  --repo "$MANAGE_SECRETS_GITHUB_REPO" \
  -f persona=<PERSONA> \
  -f secret_key=<KEY> \
  -f secret_value=<VALUE>
```

Where:
- `<PERSONA>` is this agent's persona name. Determine it from the Tailscale hostname (`tailscale status --self --json | jq -r .Self.HostName` → strip the `moltbot-` prefix) or the Kubernetes namespace (`moltbot-<persona>`)
- `<KEY>` must match `^[A-Z][A-Z0-9_]*$` (e.g., `TELEGRAM_BOT_TOKEN`, `GOOGLE_API_KEY`)
- `<VALUE>` is the secret value to set

## Monitor Workflow Status

After triggering, wait a few seconds then check status:

```bash
export GITHUB_TOKEN="$AGENT_GITHUB_PAT"
gh run list \
  --repo "$MANAGE_SECRETS_GITHUB_REPO" \
  --workflow set-secret.yml \
  --limit 3
```

To watch a specific run until completion:

```bash
export GITHUB_TOKEN="$AGENT_GITHUB_PAT"
gh run watch <RUN_ID> \
  --repo "$MANAGE_SECRETS_GITHUB_REPO"
```

## RBAC

The workflow enforces an RBAC matrix that maps GitHub usernames to allowed personas. Each persona's GitHub user can only set secrets for its own persona; admin users have wildcard access to all personas. Check the `set-secret.yml` workflow source for the current RBAC matrix.

Example RBAC structure:
```json
{
  "admin-user": ["*"],
  "bot-user[bot]": ["*"],
  "persona-a-user": ["persona-a"],
  "persona-b-user": ["persona-b"]
}
```

## Important Notes

- The workflow runs with `concurrency: { group: set-secret, cancel-in-progress: false }` — concurrent dispatches are serialized, not cancelled
- The secret key must already be a valid uppercase env var name; the workflow rejects invalid formats
- After the workflow commits, it pushes to `main`, which triggers the deploy workflow for the affected persona
- `AGENT_GITHUB_PAT` and `MANAGE_SECRETS_GITHUB_REPO` must be set in the environment; the skill has no fallback
- If the secret value is unchanged, the workflow exits cleanly with no commit
