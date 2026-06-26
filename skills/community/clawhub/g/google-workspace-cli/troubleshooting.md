# Troubleshooting - Google Workspace CLI

## 403 accessNotConfigured

Symptom: API call fails with reason `accessNotConfigured`.

Fix:
- open the `enable_url` from error payload
- enable the API in the target project
- wait briefly and retry

## OAuth restricted_client or consent failure

Symptom: login blocked in unverified app flow.

Fix:
- reduce scopes for initial login
- use testing mode and add user as test user
- expand scopes only when needed

## Wrong account used for command

Symptom: data appears from unexpected tenant.

Fix:
- check `gws auth list`
- set explicit default via `gws auth default <email>`
- use `--account` for one-off override

## Invalid params or body JSON

Symptom: 400 error with missing or invalid field.

Fix:
- run `gws schema <service.resource.method>`
- align `--params` and `--json` keys with schema
- verify path params are included

## Discovery command mismatch

Symptom: expected method not found.

Fix:
- verify service alias and API version
- retry after cache refresh window
- use `<api>:<version>` syntax for explicit version overrides
