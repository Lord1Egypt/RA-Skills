# Onboarding reference

The full signup, token-management, and storage flow for the Open Agent Guide
public API. The main SKILL.md gives the happy path; this file covers the edges.

## Signup payload

`POST /api/v1/users/signup/`

| Field                | Required    | Notes                                                                                                                                         |
| -------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `username`           | yes         | Public handle. Must satisfy Django's username rules.                                                                                          |
| `email`              | yes         | Used for account recovery. Not auto-verified at signup.                                                                                       |
| `password`           | yes         | Validated against Django's password validators. Weak passwords return `400` with `code: MISSING_REQUIRED_FIELD` or a validators-detail array. |
| `name`               | yes         | Display name.                                                                                                                                 |
| `account_type`       | yes         | `individual` or `organization`.                                                                                                               |
| `token_name`         | recommended | Friendly name for the initial token (e.g. `cli-laptop`, `ci-prod`). Defaults to a generic label.                                              |
| `token_callback_url` | no          | Default callback URL used when this token signs callback requests.                                                                            |

## Signup response

```json
{
  "user": { "id": "…", "username": "…", "email": "…", "…": "…" },
  "api_token": {
    "id": "<token-uuid>",
    "name": "first-token",
    "default_callback_url": null,
    "created_at": "2026-06-04T12:00:00Z",
    "updated_at": "2026-06-04T12:00:00Z",
    "last_used_at": null,
    "revoked_at": null,
    "bearer_token": "oag_…",
    "authorization_header": "Bearer oag_…"
  },
  "next_steps": {
    "current_user_url": "/api/v1/users/me/",
    "submission_targets_url": "/api/v1/submissions/targets/",
    "submission_fields_url_template": "/api/v1/submissions/fields/?app_label={app_label}&model={model}&view=summary",
    "create_submission_url": "/api/v1/submissions/",
    "docs_url": "/api/v1/docs/"
  }
}
```

`bearer_token` is the only place the raw value appears. Capture it before
discarding the response.

## Storing the token

### Local shell — env file

```sh
umask 077
mkdir -p ~/.config/open-agent-guide
cat > ~/.config/open-agent-guide/env <<'EOF'
export OAG_TOKEN='oag_…'
export OAG_BASE_URL='https://www.openagentguide.com'
EOF
chmod 600 ~/.config/open-agent-guide/env

# Source it from ~/.zshrc or ~/.bashrc:
#   [ -f ~/.config/open-agent-guide/env ] && . ~/.config/open-agent-guide/env
```

### macOS keychain

```sh
security add-generic-password -a "$USER" -s oag-token -w "oag_…"

# In your shell rc:
#   export OAG_TOKEN="$(security find-generic-password -a "$USER" -s oag-token -w)"
```

### Linux secret-tool (libsecret)

```sh
printf 'oag_…' | secret-tool store --label "Open Agent Guide" service oag user "$USER"

# In your shell rc:
#   export OAG_TOKEN="$(secret-tool lookup service oag user "$USER")"
```

### OpenClaw agent

`metadata.openclaw.primaryEnv: OAG_TOKEN` in SKILL.md (already declared) signals
to OpenClaw that the skill expects `OAG_TOKEN` and where to source it. Store the
token in OpenClaw's secret store; the agent injects it into the skill
environment at activation. The skill never asks the user to paste the token at
the prompt.

### GitHub Actions

```yaml
jobs:
  call-api:
    runs-on: ubuntu-latest
    steps:
      - name: Query catalog
        env:
          OAG_TOKEN: ${{ secrets.OAG_TOKEN }}
        run: |
          curl -fsSL "https://www.openagentguide.com/api/v1/users/me/" \
            -H "Authorization: Bearer ${OAG_TOKEN}"
```

Set the secret once with `gh secret set OAG_TOKEN --body "oag_…"`.

## Multiple named tokens

Issue separate tokens per workload so revoking one does not break the others:

```sh
curl -fsSL -X POST "$OAG_BASE_URL/api/v1/users/me/tokens/" \
  -H "Authorization: Bearer ${OAG_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{ "name": "ci-prod" }'
```

The response shape matches the signup `api_token` block, including
`bearer_token`. The raw value still appears only once.

Conventions that help on rotation:

- One token per host or workload (`cli-laptop`, `ci-prod`, `cron-eu`).
- Name them by *where they live*, not *what they do* — purpose drifts; host
  doesn't.
- Set `default_callback_url` per token when callbacks differ between
  environments.

## Rotation

```sh
curl -fsSL -X POST "$OAG_BASE_URL/api/v1/users/me/tokens/<token-id>/rotate/" \
  -H "Authorization: Bearer ${OAG_TOKEN}" | jq '.bearer_token'
```

The previous bearer stops working immediately. Update your secret store before
moving on; running workloads using the old value will start returning `401`.

## Revocation

```sh
curl -fsSL -X DELETE "$OAG_BASE_URL/api/v1/users/me/tokens/<token-id>/" \
  -H "Authorization: Bearer ${OAG_TOKEN}"
```

A revoked token cannot be restored. Issue a new one if you revoked the wrong id.

## Forgot the bearer value

Bearer values are not retrievable after the original response. The token
metadata endpoints (`GET /me/tokens/`, `GET /me/tokens/<id>/`) return
identifiers and timestamps only. If you lost a bearer, rotate the token to mint
a new one.

## When auth breaks

| Symptom                               | Likely cause                               | Fix                                                       |
| ------------------------------------- | ------------------------------------------ | --------------------------------------------------------- |
| `401` on every authenticated call     | Token revoked, rotated, or never persisted | Re-read `OAG_TOKEN` from secret store; rotate if stale    |
| `401` only after a deploy             | Stale secret in CI                         | Re-set the repository secret with the rotated value       |
| `429 rate_limited` at signup          | Hit the 10/hour-per-IP cap                 | Wait for `Retry-After`; signups are per-IP, not per-token |
| `400 MISSING_REQUIRED_FIELD password` | Password fails Django validators           | Provide a stronger password                               |
