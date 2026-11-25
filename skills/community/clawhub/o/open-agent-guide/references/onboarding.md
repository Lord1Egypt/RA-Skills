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

Both `bearer_token` and `authorization_header` contain the secret. Store the
bearer before discarding the response.

## Create and store a token

Choose a user-approved secret store before signup. Capture and validate each
token in memory before writing to that store. A failed request or invalid
response must leave the stored secret unchanged. Do not print `bearer_token` or
`authorization_header`. Do not save raw responses to disk. Disable shell
tracing, session recording, and HTTP debug output first.

The following example runs in an interactive Bash terminal with `curl`, `jq`,
and Linux `secret-tool` installed. It prompts for signup fields and sends the
password through standard input. It stores the bearer directly in libsecret.
Check that the secret store is unlocked and writable before creating the
account. Run this only when the user has authorized signup and credential
storage.

```bash
(
  set +x
  set -euo pipefail
  command -v secret-tool >/dev/null
  export OAG_SIGNUP_USERNAME OAG_SIGNUP_EMAIL OAG_SIGNUP_NAME OAG_SIGNUP_PASSWORD
  read -r -p 'Username: ' OAG_SIGNUP_USERNAME
  read -r -p 'Email: ' OAG_SIGNUP_EMAIL
  read -r -p 'Display name: ' OAG_SIGNUP_NAME
  read -r -s -p 'Password: ' OAG_SIGNUP_PASSWORD
  printf '\n' >&2
  new_token="$(
    jq -n '{username: env.OAG_SIGNUP_USERNAME, email: env.OAG_SIGNUP_EMAIL,
            name: env.OAG_SIGNUP_NAME, password: env.OAG_SIGNUP_PASSWORD,
            account_type: "individual", token_name: "local-shell"}' |
      curl -fsS --proto '=https' -X POST \
        'https://www.openagentguide.com/api/v1/users/signup/' \
        -H 'Content-Type: application/json' --data-binary @- |
      jq -er '.api_token.bearer_token | strings | select(startswith("oag_"))'
  )"
  printf '%s' "$new_token" |
    secret-tool store --label 'Open Agent Guide' service oag user "$USER"
)
```

If the request or storage fails, stop. The account may already exist. Use
account recovery to issue a replacement token; do not repeat signup
automatically. Signup allows 10 requests per hour per IP. Respect `Retry-After`
on HTTP 429.

Load the stored token without printing it, with tracing disabled:

```bash
set +x
OAG_TOKEN="$(secret-tool lookup service oag user "$USER")"
export OAG_TOKEN
```

For macOS Keychain, OpenClaw, or a CI secret store, use the host's approved
secret entry mechanism. Verify how the host injects `OAG_TOKEN` before
authenticated use. `metadata.openclaw.primaryEnv` declares the variable; it does
not itself store a credential or enforce runtime permissions. Do not paste
credentials into chat or command arguments. For a local env file, use a private
directory and mode 600, and keep it outside the repository. Do not change
startup files without user authorization.

## Multiple named tokens

Issue separate tokens per workload so revoking one does not break the others.
With the libsecret setup above, capture the new token under a separate key. Run
this example in Bash:

```bash
(
  set +x
  set -euo pipefail
  new_token="$(
    curl -fsS -X POST "$OAG_BASE_URL/api/v1/users/me/tokens/" \
      -H "Authorization: Bearer ${OAG_TOKEN}" \
      -H "Content-Type: application/json" \
      -d '{ "name": "ci-prod" }' |
      jq -er '.bearer_token | strings | select(startswith("oag_"))'
  )"
  printf '%s' "$new_token" |
    secret-tool store --label 'Open Agent Guide CI' service oag workload ci-prod
)
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

Rotate only the token selected by the user or the authorized recovery task. The
example replaces the local-shell secret. Run it in Bash. Confirm that libsecret
is writable first.

```bash
(
  set +x
  set -euo pipefail
  new_token="$(
    curl -fsS -X POST "$OAG_BASE_URL/api/v1/users/me/tokens/<token-id>/rotate/" \
      -H "Authorization: Bearer ${OAG_TOKEN}" |
      jq -er '.bearer_token | strings | select(startswith("oag_"))'
  )"
  printf '%s' "$new_token" |
    secret-tool store --label 'Open Agent Guide' service oag user "$USER"
)
```

The previous bearer stops working immediately. Update your secret store before
moving on. Reload `OAG_TOKEN` from the store. If storage fails, stop and use
account recovery; the old token is already invalid. Running workloads using the
old value will start returning `401`.

## Revocation

```sh
curl -fsS -X DELETE "$OAG_BASE_URL/api/v1/users/me/tokens/<token-id>/" \
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
