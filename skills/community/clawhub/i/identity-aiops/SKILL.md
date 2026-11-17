---
name: identity-aiops
slug: identity-aiops
displayName: "Identity AIops"
summary: "Governed Keycloak + authentik identity ops: users, events, clients, MFA, RCA. 29 tools."
license: MIT
homepage: https://github.com/AIops-tools/Identity-AIops
tags: [aiops, mcp, governance, identity]
description: >
  Use this skill whenever the user needs to operate a Keycloak or authentik identity provider — a one-shot overview, realm settings, users with sessions/credentials/groups/lockout status, authentication and admin events, OAuth/OIDC clients, four flagship RCAs (login-failure/lockout-storm, stale access, client misconfiguration, MFA coverage), and governed writes (disable/enable a user, revoke sessions, require a password reset, replace redirect URIs, rotate a client secret).
  Always use this skill for "Keycloak", "authentik", "realm", "SSO users", "login failures", "brute force logins", "locked out users", "stale accounts", "service account misuse", "redirect URI", "PKCE", "implicit flow", "client secret rotation", "MFA coverage", "who has no 2FA" when the context is a Keycloak/authentik IdP.
  Do NOT use when the target is something other than a Keycloak/authentik identity provider (a hypervisor, storage appliance, backup product, container-orchestration cluster, firewall, database, or OT/industrial equipment) — route those to the appropriate other AIops-tools skill. Cloud IdPs (Okta, Entra ID, Auth0) are out of scope.
  Governed identity operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers).
installer:
  kind: uv
  package: identity-aiops
argument-hint: "[a user/client id, a realm, or describe your identity task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["identity-aiops","uvx"]},"optional":{"env":["IDENTITY_AIOPS_CONFIG","IDENTITY_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/Identity-AIops","emoji":"🔐","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed identity-provider operations across Keycloak (admin REST API /admin/realms/{realm}/..., OAuth2 client-credentials grant against the realm token endpoint with automatic refresh-on-401) and authentik (API v3 /api/v3/..., long-lived API token as a Bearer header). Each target in the config names its own platform, and a name-keyed platform registry selects the API shape, so the same tools work on both and one config can span a mixed estate. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  All write operations are audited to a local SQLite DB under ~/.identity-aiops/ (relocatable via IDENTITY_AIOPS_HOME).
  Credentials: the Keycloak confidential client's client secret or the authentik API token is stored ENCRYPTED in ~/.identity-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'identity-aiops init' to onboard (it asks for the platform, base URL, and — Keycloak — realm + client_id), or 'identity-aiops secret set <target>' to add one. The store is unlocked by a master password from IDENTITY_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var IDENTITY_<TARGET_NAME_UPPER>_SECRET is still honoured as a fallback with a deprecation warning (migrate with 'identity-aiops secret migrate'). Secrets are held only in memory, never logged or echoed; rotate_client_secret returns and records masked fingerprints only.
  State-changing operations pass through the @governed_tool decorator (budget guard + audit + risk-tier labelling). enable_user, update_client_redirect_uris, and rotate_client_secret are risk=high with dry_run; revoke_user_sessions and rotate_client_secret are irreversible (priorState only). Reversible writes (disable_user/enable_user, require_password_reset, update_client_redirect_uris) capture the real fetched before-state and record an inverse undo descriptor. The tool records every call but does not decide whether a write is permitted — that is the agent's judgement or the connecting account's permissions.
  Webhooks: none — no outbound network calls beyond the configured Keycloak / authentik REST API.
  SSL: verify_ssl defaults to ON; disable only for self-signed lab certs.
  Transitive dependencies: httpx (HTTP client) and the MCP SDK. No post-install scripts or background services.
  Verification status: mock-validated; no recorded end-to-end run against a live IdP yet, and the modelled REST paths are the largest verification debt. Both Keycloak and authentik are free/self-hostable (each runs from a single container), so a lab is the cheapest live check. See docs/VERIFICATION.md.
---

# Identity AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by the Keycloak project, Red Hat, Authentik Security Inc., or the authentik project.** Keycloak and authentik are trademarks of their respective owners. Source at [github.com/AIops-tools/Identity-AIops](https://github.com/AIops-tools/Identity-AIops) under the MIT license.

Governed identity operations — **29 MCP tools** across **Keycloak** (admin REST
`/admin/realms/{realm}/...`) and **authentik** (API v3 `/api/v3/...`), every one
wrapped with the bundled `@governed_tool` harness: a local unified audit log
under `~/.identity-aiops/`, policy engine, token/runaway budget guard,
undo-token recording, and risk-tier labelling on the audit row. A per-target
`platform` field selects the API shape, so the same tools work on both IdPs and
one config can span a mixed estate. The Keycloak client secret / authentik API
token is stored **encrypted** (`~/.identity-aiops/secrets.enc`, Fernet +
scrypt) — never plaintext on disk.

> **Standalone**: the governance harness is bundled in the package
> (`identity_aiops.governance`) — no external skill-family dependency. Both
> platforms are free/self-hostable, so a self-hosted lab is the cheapest live
> check; verification status and the checklist are in `docs/VERIFICATION.md`.

## What This Skill Does

| Group | Tools | Count | R/W |
|-------|-------|:-----:|:---:|
| **Realm / system** | identity_overview, realm_info, list_identity_providers | 3 | read |
| **Users / groups** | list_users, user_detail, user_count, user_sessions, user_credentials, list_groups, group_members, user_lockout_status | 8 | read |
| **Events** | login_events, admin_events | 2 | read |
| **Clients** | list_clients, client_detail, client_sessions, client_session_stats | 4 | read |
| **Flagship analyses** | login_failure_rca, stale_access_audit, client_misconfig_audit, mfa_coverage_analysis | 4 | read |
| **Writes** | disable_user, revoke_user_sessions, require_password_reset | 3 | write (med) |
| **Writes** | enable_user, update_client_redirect_uris, rotate_client_secret | 3 | write (**high**) |
| **Undo** | undo_list, undo_apply | 2 | read + replay |

The four flagship analyses are transparent heuristics that report their numbers,
never a black-box verdict: `login_failure_rca` windows the failed-auth feed by
user/IP/client and separates password spray, targeted brute-force, a stale
stored credential, a misconfigured client, an expired-credential storm, and a
lockout storm; `stale_access_audit` flags dormant and never-used accounts,
interactive service accounts, and orphaned sessions; `client_misconfig_audit`
ranks clients by OAuth-BCP risk (wildcard/http redirects, secrets in public
clients, implicit flow, missing PKCE, password grant); `mfa_coverage_analysis`
reports second-factor coverage overall and per group.

## Quick Install

```bash
uv tool install identity-aiops
identity-aiops init       # wizard: pick platform (keycloak/authentik) + encrypted secret
identity-aiops doctor
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/identity-aiops
openclaw skills info identity-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Get a one-shot snapshot (`overview` / `realm_info` / `user_count`)
- Triage a login-failure or lockout storm (`login_failure_rca`) → cause + action
- Run an access re-certification (`stale_access_audit`: idle users,
  never-logged-in accounts, service-account misuse, orphaned sessions)
- Audit OAuth clients (`client_misconfig_audit`: redirect URIs, PKCE, implicit
  flow, password grant) and fix them (`update_client_redirect_uris`)
- Measure and close the MFA gap (`mfa_coverage_analysis`, `user_credentials`)
- Contain a compromised account (`disable_user` + `revoke_user_sessions` +
  `require_password_reset`, all governed; re-enable is tagged high risk)
- Rotate a leaked client secret (`rotate_client_secret`, high risk, masked)

**Do NOT use when** the target is not a Keycloak/authentik IdP — route
hypervisor, storage, backup, cluster, network/firewall, database, endpoint, or
OT/industrial work to the appropriate other AIops-tools skill. Cloud IdPs
(Okta, Entra ID, Auth0) are out of scope.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| Keycloak / authentik identity ops | **identity-aiops** (this skill) |
| A non-identity platform (hypervisor, storage, backup, cluster, network device/controller, firewall, database, containers, endpoints, local LLM governance, compliance evidence) | the appropriate **other AIops-tools** skill (proxmox-aiops, truenas-aiops, ceph-aiops, veeam-aiops, k8s-aiops, network-aiops, fabric-aiops, firewall-aiops, postgres-aiops, container-host-aiops, endpoint-aiops, ai-guardian, compliance-aiops, …) |
| Cloud IdPs (Okta, Entra ID, Auth0) | out of scope for this tool |

## Common Workflows

Each recipe starts from a read or one of the four RCAs and ends in a governed
write. The **RCAs are MCP tools** (`login_failure_rca`, `stale_access_audit`,
`client_misconfig_audit`, `mfa_coverage_analysis`) — call them through the MCP
server; the CLI covers the reads and the writes. Every CLI write accepts
`--dry-run` and otherwise double-confirms.

### 1. "We're being brute-forced — contain it"

1. `identity-aiops overview` → how big is the failed-login feed right now, and
   is this one account or the whole realm?
2. MCP `login_failure_rca` → findings carrying their counts (the ordering is not on one
   comparable quantity — see `references/agent-guardrails.md`), separating password
   **spray** from one IP, **targeted** brute-force on one account, a client
   failing with credential errors (a rotated secret not deployed), an
   expired-credential storm, and a lockout storm.
3. `identity-aiops events --type LOGIN_ERROR --user <username> -n 200` → the
   raw failures behind the finding (authentik: `--type login_failed`).
4. `identity-aiops users show <user-id>` and `identity-aiops users sessions
   <user-id>` → is the account already compromised, i.e. did any attempt
   actually succeed?
5. Contain: `identity-aiops users disable <user-id> --dry-run`, then for real
   (reversible — the fetched before-state is captured and an `enable_user`
   inverse recorded).
6. `identity-aiops users revoke-sessions <user-id>` → kill live sessions.
   **Irreversible** (priorState only) — disabling alone does not end sessions
   already issued, so this step is what actually stops the attacker.
7. `identity-aiops undo list` → confirm the disable is reversible before you
   hand off.

**Failure branch**: if the RCA classifies it as a **misconfigured client**
rather than an attack (mass credential errors from one client id), do not
disable users — you would lock out legitimate people while the real fault is a
rotated secret that was never deployed. Go to recipe 3. If you disabled the
wrong account, `identity-aiops users enable <user-id>` is **high** risk and
needs `IDENTITY_AUDIT_APPROVED_BY` + `IDENTITY_AUDIT_RATIONALE`, deliberately —
re-enabling reverses containment.

### 2. "Quarterly access re-certification"

1. MCP `stale_access_audit` (e.g. `stale_days=90`) → dormant users with day
   counts, never-logged-in accounts, service accounts being used
   interactively, and orphaned sessions.
2. `identity-aiops users list --search <name>` / `identity-aiops users show
   <user-id>` → confirm each candidate is genuinely the account you think.
3. `identity-aiops users sessions <user-id>` → check for a live session before
   you touch a "dormant" account.
4. Confirm with the account owner or its manager. Then, per account:
   `identity-aiops users disable <user-id>` (reversible, undo-recorded).
5. `identity-aiops users revoke-sessions <user-id>` for the orphaned sessions
   the audit found (irreversible).
6. Re-run `stale_access_audit` to confirm the list shrank as expected.

**Failure branch**: an **interactive service account** finding is not a
disable candidate — disabling it takes down whatever integration depends on
it. Trace the client first (`identity-aiops clients show <client-id>`,
`identity-aiops clients list`) and fix the integration to stop using
interactive login. If a disable breaks something unexpectedly,
`identity-aiops undo apply <id>` replays the captured prior state.

### 3. "Harden the OAuth clients before the audit"

1. MCP `client_misconfig_audit` → per-client `riskScore` with the evidence
   behind it: wildcard or plain-`http` redirect URIs, a public client holding
   a secret, implicit flow enabled, missing PKCE, password grant allowed.
2. `identity-aiops clients show <client-id>` → the full current client
   configuration, so you replace the right values.
3. `identity-aiops clients set-redirect-uris <client-id> --uri
   https://app.example.com/callback --dry-run` → note that `--uri` is repeated
   and supplies the **FULL new list**, replacing what is there.
4. Re-run without `--dry-run`: **high** risk, double confirm, requires
   `IDENTITY_AUDIT_APPROVED_BY` + `IDENTITY_AUDIT_RATIONALE`. The prior URI
   list is captured, so undo replays it exactly.
5. If a secret leaked: `identity-aiops clients rotate-secret <client-id>`
   (**high** risk, **irreversible**, masked priorState) — then deploy the new
   secret everywhere that client is used.
6. Re-run `client_misconfig_audit` to confirm the score dropped.

**Failure branch**: rotating a secret before the deployments are ready is how
you cause recipe 1's "misconfigured client" storm — every service using the old
secret starts failing authentication immediately, and rotation cannot be
undone. Stage the deployment first. If a redirect-URI replacement breaks a
login flow, `identity-aiops undo apply <id>` restores the exact prior list;
this is why the URI change is reversible and the rotation is not.

### 4. "Show me who still has no second factor"

1. MCP `mfa_coverage_analysis` → coverage percentage, the worst groups first,
   and the per-user gap list.
2. `identity-aiops users credentials <user-id>` → what a specific user
   actually has configured, so you distinguish "no MFA" from "an enrolled
   factor the analysis could not see".
3. `identity-aiops overview` and realm settings → confirm the realm's
   brute-force protection and OTP policy actually require what you think they
   require.
4. Where a forced re-enrolment is part of the rollout:
   `identity-aiops users require-reset <user-id> --dry-run`, then for real
   (reversible — undo clears the pending requirement).
5. `identity-aiops undo list` → confirm each reset flag can be cleared if the
   rollout stalls.

**Failure branch**: if a user is blocked out by the reset requirement (no
working recovery path, or they cannot complete enrolment),
`identity-aiops users require-reset <user-id> --clear` removes the pending
requirement, and `identity-aiops undo apply <id>` does the same from the
recorded token. Do not chase a 100% coverage number by forcing resets on
service accounts — they have no interactive user to complete the flow, and the
`stale_access_audit` in recipe 2 is the right tool for those.

## Governance & Safety

The skill delivers reads and writes and records them; it does **not** decide
whether a write is permitted. That is your agent's judgement, or the permission
of the account you connect it with (a Keycloak service account or authentik
token without `manage-*` scope — writes then fail at the server). There is no
read-only switch, policy file, or approval gate.

- **Audit is the guarantee, and it is not bypassable.** Every call — MCP and
  CLI alike — lands an audit row in `~/.identity-aiops/audit.db` (relocatable
  via `IDENTITY_AIOPS_HOME`): params, status, and the risk tier.
- `IDENTITY_AUDIT_APPROVED_BY` / `IDENTITY_AUDIT_RATIONALE` are optional
  annotations recorded on the row (who/why); they are never required and never
  block.
- **Risk tier** — a descriptive label on the audit row derived from
  `risk_level` (`enable_user`, `update_client_redirect_uris`,
  `rotate_client_secret` = high; `disable_user`, `revoke_user_sessions`,
  `require_password_reset` = medium); it gates nothing. Writes support
  `--dry-run` and double confirmation at the CLI.
- Reversible writes capture the real fetched before-state and record an
  inverse descriptor (disable↔enable, reset-flag→clear, redirect-URI list
  replay). `revoke_user_sessions` and `rotate_client_secret` are irreversible
  (priorState only; secrets recorded masked).

## References

- `references/capabilities.md` — full tool + platform + API-path reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, and connectivity
- `references/agent-guardrails.md` — running with a smaller / local model: the
  truncation and null-field contracts, the Keycloak-vs-authentik tool
  asymmetry, and a system prompt
