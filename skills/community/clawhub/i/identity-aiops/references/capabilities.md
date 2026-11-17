# identity-aiops capabilities

> **29 MCP tools** (21 read, 6 write, 2 undo) across Keycloak (admin REST `/admin/realms/{realm}/...`,
> client-credentials grant, refresh-on-401) and authentik (API v3 `/api/v3/...`,
> Bearer token). The concrete REST paths below are modelled from each project's
> public API and need live verification.

A per-target `platform` field (`keycloak` / `authentik`) selects the API shape;
the same tool name resolves to the right path on each IdP via the platform
registry. Every substituted path segment (realm, user id, client id) is
percent-encoded centrally.

## Realm / system (read)

| Tool | Keycloak path | authentik path | Returns |
|------|---------------|----------------|---------|
| `identity_overview` | (composite) | (composite) | platform/realm, user/client/IdP counts, failed-login feed size |
| `realm_info` | `/admin/realms/{realm}` | `/api/v3/admin/system/` | brute-force protection, password/OTP policy (KC); version/environment (AK) |
| `list_identity_providers` | `/admin/realms/{realm}/identity-provider/instances` | `/api/v3/sources/all/` | federated IdPs / sources with enabled state |

## Users / groups (read)

| Tool | Keycloak path | authentik path | Returns |
|------|---------------|----------------|---------|
| `list_users` | `/admin/realms/{realm}/users` | `/api/v3/core/users/` | normalized users (id, username, enabled, lastLogin, serviceAccount) |
| `user_detail` | `/admin/realms/{realm}/users/{id}` | `/api/v3/core/users/{id}/` | one user incl. requiredActions/attributes |
| `user_count` | `/admin/realms/{realm}/users/count` | `/api/v3/core/users/` (pagination.count) | total users — the doctor probe |
| `user_sessions` | `/admin/realms/{realm}/users/{id}/sessions` | `/api/v3/core/authenticated_sessions/?user=` | active sessions (id, IP, start/last access) |
| `user_credentials` | `/admin/realms/{realm}/users/{id}/credentials` | `/api/v3/authenticators/admin/all/?user=` | credentials/devices with second-factor flags |
| `list_groups` | `/admin/realms/{realm}/groups` | `/api/v3/core/groups/` | groups |
| `group_members` | `/admin/realms/{realm}/groups/{id}/members` | `/api/v3/core/groups/{id}/` (users_obj) | normalized member users |
| `user_lockout_status` | `/admin/realms/{realm}/attack-detection/brute-force/users/{id}` | — (teaching error) | failure count, locked state, last failure IP |

## Events (read)

| Tool | Keycloak path | authentik path | Returns |
|------|---------------|----------------|---------|
| `login_events` | `/admin/realms/{realm}/events` | `/api/v3/events/events/` | normalized events {time, type, user, ip, client, error} |
| `admin_events` | `/admin/realms/{realm}/admin-events` | `/api/v3/events/events/` (admin actions) | admin/config changes {operation, resource, actor, ip} |

## Clients (read)

| Tool | Keycloak path | authentik path | Returns |
|------|---------------|----------------|---------|
| `list_clients` | `/admin/realms/{realm}/clients` | `/api/v3/providers/oauth2/` | normalized clients (public flag, redirect URIs, flows, PKCE) |
| `client_detail` | `/admin/realms/{realm}/clients/{id}` | `/api/v3/providers/oauth2/{id}/` | one client normalized |
| `client_sessions` | `/admin/realms/{realm}/clients/{id}/user-sessions` | — (teaching error) | sessions on one client |
| `client_session_stats` | `/admin/realms/{realm}/client-session-stats` | — (teaching error) | active-session counts per client |

## Flagship analyses (read, pure heuristics over the reads)

| Tool | Feed | Findings |
|------|------|----------|
| `login_failure_rca` | failed-login events (windowed) | password-spray (one IP → many users), targeted-brute-force (many IPs → one user), stale-stored-credential (one IP → one user), misconfigured-client (client-credential errors), expired-credential-storm, lockout-storm — each with counts, cause, action; thresholds included in output |
| `stale_access_audit` | users + successful logins + sessions | staleUsers (idle > N days), neverLoggedIn, serviceAccountsInteractive, orphanedSessions |
| `client_misconfig_audit` | normalized clients | wildcard-redirect-uri, http-redirect-uri (non-localhost), public-client-with-secret, implicit-flow-enabled, public-client-missing-pkce, password-grant-enabled — ranked riskScore (high=30/med=15/low=5); `checksNotEvaluated` counts checks skipped because the IdP does not report their input (authentik providers have no implicit-flow or password-grant toggle) — a clean result is not a pass for those |
| `mfa_coverage_analysis` | users + per-user credentials | coverage % overall/per group, usersWithoutMfa; second factors = otp/totp/hotp/webauthn/duo/sms (confirmed) |

## Writes (governed: dry_run preview, audit, undo where reversible)

| Tool | Risk | Keycloak call | authentik call | Undo |
|------|:----:|---------------|----------------|------|
| `disable_user` | med | `PUT users/{id}` `{enabled:false}` | `PATCH core/users/{id}/` `{is_active:false}` | `enable_user` (only if it was enabled) |
| `enable_user` | **high** | `PUT users/{id}` `{enabled:true}` | `PATCH core/users/{id}/` `{is_active:true}` | `disable_user` (only if it was disabled) |
| `revoke_user_sessions` | med | `POST users/{id}/logout` | `DELETE authenticated_sessions/{sid}/` each | none — priorState sessionCount |
| `require_password_reset` | med | `PUT users/{id}` requiredActions ± UPDATE_PASSWORD | — (teaching error) | itself with `clear=True` (only if this call set it) |
| `update_client_redirect_uris` | **high** | `PUT clients/{id}` `{redirectUris}` | `PATCH providers/oauth2/{id}/` `{redirect_uris}` | itself with the prior list |
| `rotate_client_secret` | **high** | `GET`+`POST clients/{id}/client-secret` | — (teaching error) | none — priorState **masked** fingerprint |

Risk-tier rationale: containment/hygiene actions an operator needs promptly
(disable, revoke, require-reset) sit at medium; access-granting or
boundary-replacing actions (enable, redirect-URI replace, secret rotation) sit
at high. The tier is a descriptive label carried onto the audit row, not a
gate — whether a write runs is the agent's judgement or the connecting
account's permissions.
