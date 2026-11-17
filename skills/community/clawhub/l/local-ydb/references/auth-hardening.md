# Auth Hardening Reference

## Target Posture

Recommended hardened posture for demo-style local-ydb deployments:

- internal-only: YDB static-node gRPC `2136`
- internal-only: dynamic-node gRPC ports such as `2137`, `2138`, `2139`
- loopback-only: YDB monitoring backend `127.0.0.1:8765`
- optional public monitoring only through HTTPS reverse proxy
- YDB native auth enabled with `security_config.enforce_user_token_requirement: true`
- monitoring/viewer/admin ACLs restricted to admin SIDs such as `root` and `root@builtin`

This posture intentionally does not provide public direct YDB client access.

## User Credentials

Static username/password examples should use generic placeholders:

```bash
YDB_STATIC_CREDENTIALS_USER=<app-user>
YDB_STATIC_CREDENTIALS_PASSWORD_FILE=/run/secrets/<app-user>.password
YDB_STATIC_CREDENTIALS_AUTH_ENDPOINT=grpc://ydb-local:2136
```

Use environment-variable passwords only as a fallback when a password file is not available. For private-CA TLS, set `YDB_SSL_ROOT_CERTIFICATES_FILE`.

Keep password files, tokens, CA private keys, and host-specific secret paths outside git.

Field-proven default-root behavior on `local-ydb` images:

- generated `security_config.default_users` can contain `root` with password `1234`
- Never use the known default root password outside an isolated test. Rotate it to a unique non-default password, verify rotation, and retire obsolete credential copies before admitting clients or exposing monitoring to other users. Restricted retention archives follow the policy below.
- a token minted from that username/password can identify as `User SID: root`
- dynamic-node auth token files can still use `root@builtin`

Because of that split identity, viewer/monitoring/admin/register-dynamic-node ACLs should usually include both `root` and `root@builtin` unless the deployed build proves a different SID mapping.

## Password Policy

Upstream YDB defaults to no password complexity requirements. In the default posture:

- empty passwords are allowed by YDB itself through `PASSWORD NULL` or equivalent SQL
- existing passwords keep working if a stricter policy is configured later
- special-character guidance in YDB docs is based on `!@#$%^&*()_+{}|<>?=`

Clusters can still tighten this through `auth_config.password_complexity`, for example:

- `min_length`
- `min_lower_case_count`
- `min_upper_case_count`
- `min_numbers_count`
- `min_special_chars_count`
- `special_chars`

Operational guidance for this toolkit:

- `local_ydb_set_root_password` requires a non-empty password value even though upstream YDB can allow an empty password
- if rotation fails with a password-policy error, inspect the active `auth_config.password_complexity` in the generated `config.yaml` before retrying
- prefer letters, digits, and documented YDB special characters unless the target build has already been rehearsed with a wider character set

## Dynamic Node Auth

For a mandatory-auth local-ydb dynamic node, `--auth-token-file` is a text protobuf for `NKikimrProto.TAuthConfig`, not a raw access-token file. Two fields matter during startup:

- `NodeRegistrationToken` is used while registering the dynamic node.
- `StaffApiUserToken` is used later when the node fetches dynamic config through `GetNodeConfig`.

The file shape is:

```text
StaffApiUserToken: "<allowed-node-sid>"
NodeRegistrationToken: "<allowed-node-sid>"
```

This can avoid mounting password files into dynamic-node containers when the SID is already allowed by `security_config.register_dynamic_node_allowed_sids`. Certificate-based node authorization is still the stricter production pattern.

To check what SID a username/password token represents without printing the token:

```bash
(
set -euo pipefail
umask 077
password_input=$(mktemp)
cleanup_input() { rm -f -- "$password_input"; }
trap cleanup_input EXIT
trap "exit 130" INT
trap "exit 143" TERM
sudo cat /path/to/root.password >"$password_input"
test -s "$password_input"
docker exec -i ydb-local bash -lc '
  set -euo pipefail
  umask 077
  credentials_dir=$(mktemp -d)
  cleanup() {
    rm -f -- "$credentials_dir/root.password" "$credentials_dir/root.token"
    rmdir -- "$credentials_dir"
  }
  trap cleanup EXIT
  trap "exit 130" INT
  trap "exit 143" TERM
  cat >"$credentials_dir/root.password"
  test -s "$credentials_dir/root.password"
  /ydb -e grpc://localhost:2136 -d /local \
    --user root \
    --password-file "$credentials_dir/root.password" \
    auth get-token -f >"$credentials_dir/root.token"
  test -s "$credentials_dir/root.token"
  /ydbd --server localhost:2136 --token-file "$credentials_dir/root.token" whoami
' <"$password_input"
)
```

## Rollout Sequence

For production-like changes, use a copied volume first when possible. Keep application clients stopped and public monitoring inaccessible until all acceptance checks pass; loopback alone does not isolate the stack from other local users and processes.

1. Save current container definitions and current YDB config.
2. Back up the Docker volume or bind-mounted data directory before patching config.
3. Create or verify users before enforcing auth.
4. Grant application users only the tenant access they need, commonly `ydb.generic.use` on `/local/<tenant>`.
5. Patch YDB config to enforce native auth and tighten viewer, monitoring, admin, bootstrap, and dynamic-node registration SIDs.
6. Stop containers in dependency order: clients, dynamic nodes, static node.
7. Start only the static node, then the dynamic nodes; keep clients stopped and public monitoring inaccessible.
8. Rotate the root password using Scenario 10A below: review the plan, then confirm execution on the isolated auth-enabled stack.
9. Verify rotation using the complete success criteria below, including fresh new-password success and old-password rejection.
10. Verify tenant state, GraphShard, anonymous denial, and authenticated behavior with the new credentials.
11. Retire obsolete credential backups after the explicit rollback hold is closed, using the policy below.
12. Admit clients or enable the reviewed public monitoring route only after steps 9-11 pass.

Before step 6 mutates config or container state, require the full check-only static compatibility preflight to pass for the profile image, network, data mount, environment, restart policy, healthcheck, and exact configured loopback bindings. An immutable mismatch leaves the stack untouched and requires destroy followed by bootstrap.

When `dynamicNodeCount > 1`, steps 6-7 and 10 apply to every configured dynamic node. Stop all configured nodes before restarting the static node, then recreate nodes `1..N` in index order, with the auth-token mount when one is configured and without it otherwise. This recreate path also restores a missing configured node. After each launch, the exact container must be stably running and authenticated or anonymous `viewer/json/nodelist`, as appropriate for the profile, must contain its configured IC port before the next node starts. One-off suffixes above `dynamicNodeCount` keep their existing standalone hardening policy; this declarative rollout does not broaden it. If rollback restores the prior static config, use `local_ydb_restart_stack` or `local_ydb_bootstrap` to recreate configured nodes; `docker start` cannot recover definitions removed by hardening.

Before mutating live config or volumes, provide a rollback plan: previous run commands, previous image tag, volume backup, and config restore point.

Recommended MCP sequence for a fresh stable `26.1.1.6` GHCR stack:

1. `local_ydb_dump_tenant(confirm=true, dumpName="pre-auth-...")`
2. bootstrap a fresh clean stack on separate container names, network, volume, and ports with exact image `ghcr.io/ydb-platform/local-ydb:26.1.1.6`
3. `local_ydb_restore_tenant(confirm=true, dumpName="pre-auth-...")`
4. `local_ydb_prepare_auth_config(confirm=true)` to extract current config and root password file
5. `local_ydb_write_dynamic_auth_config(confirm=true)` for the dynamic auth text-proto
6. `local_ydb_apply_auth_hardening(confirm=true)` on the same stack
7. `local_ydb_set_root_password(confirm=false, password="<new-password>")` to review the rotation plan
8. `local_ydb_set_root_password(confirm=true, password="<new-password>")` only after approving that plan
9. verify rotation using Scenario 10A, then run Scenario 10 with the new credentials; close the rollback hold and retire obsolete credential backups before admitting clients or exposing monitoring

For rotation, the selected profile must have `authConfigPath` and `rootPasswordFile`; prepare them before enforcing auth. Follow [Scenario 10A](mcp-tool-scenarios.md#scenario-10a-root-password-rotation), then [Scenario 10](mcp-tool-scenarios.md#scenario-10-post-auth-verification). Rotation runs after auth is enabled because the tool also verifies anonymous denial.

Rotation acceptance requires all four execution results to be successful, the host auth config and password file to match the new credential, a fresh login with the new password to succeed, a fresh login with the old password to be rejected, and anonymous viewer access to remain `401`. `executed: true` alone is not success. Keep passwords in protected files for checks, never argv or logs. Use new sessions without cached cookies or tokens; check lockout policy before the single negative login attempt. A timeout, transport failure or unavailable endpoint does not prove old-password rejection. Password-login rejection does not prove revocation of previously issued tokens; see [YDB authentication](https://ydb.tech/docs/en/security/authentication).

Keep the stack isolated if rotation partially fails or its outcome is unknown. The runtime password can change before host artifacts are synchronized. Establish which credential currently authenticates and whether host config/password files match before recovery. Do not retry blindly or automatically restore the weak default password.

## Obsolete Credential Backups

Successful `local_ydb_set_root_password` leaves `${authConfigPath}.before-local-ydb-toolkit-password-rotate` and `${rootPasswordFile}.before-local-ydb-toolkit-password-rotate` when the corresponding original files existed. The tool does not retire these backups. Its rollback suggestions can copy them back into active use.

After fresh new-password success, old-password rejection and post-auth verification, complete this step before client admission:

1. Inventory those two exact profile-derived paths, the protected old-password verification file, and any earlier config copies containing the old credential. Do not print their contents or select files with wildcard cleanup.
2. Assign an owner and deadline to an explicit rollback hold. Keep the stack isolated while that hold is open; the owner must close it after verified recovery readiness, not just because a timer expired.
3. Under an approved secret-retention policy, delete the obsolete files using the storage-appropriate deletion procedure or move them to an encrypted, access-restricted archive outside the active config directories. An archive record must identify its owner, retention deadline, and approved deletion procedure. Replace ordinary rollback pointers so they cannot select these obsolete files automatically.
4. Verify that the obsolete paths are absent from the operational locations and record their retirement without recording credentials. Restoring any retained archive requires a separately approved isolated recovery and a new non-default password before admission; never automatically restore the known default. If retirement or verification fails, keep clients stopped and monitoring isolated.

This policy applies to the retained backup copies as well as the temporary negative-login credential. Filesystem deletion alone does not prove erasure from snapshots or storage media; include those copies in the chosen retention procedure. See [OWASP secrets backup and restore guidance](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html#29-downtime-break-glass-backup-and-restore).

## Monitoring Exposure

YDB itself should remain the source of truth for authorization. A reverse proxy may provide HTTPS transport and routing, but do not rely on proxy Basic Auth as the only protection for YDB monitoring data.

If the YDB frontend is proxied under a path prefix, it can call several top-level backend routes. Proxy route families may include:

- `/login`
- `/logout`
- `/viewer`
- `/node/`
- `/storage/`
- `/operation/`
- `/query/`
- `/scheme/`
- `/pdisk/`
- `/vdisk/`

Protected JSON endpoints such as `/viewer/json/tenants` should reject anonymous requests with `401` in the hardened topology. Bearer-token testing against these endpoints may return `Token is not supported`; prefer the built-in YDB UI login flow unless official YDB docs for the deployed version say otherwise.

Observed login shape on some builds:

- `POST /login` accepts JSON with `{"user":"root","password":"..."}`
- cookie-based requests to protected viewer endpoints work after login
- protected endpoints may redirect with `307`; use `curl -L` in scripts
- use the actual monitoring port from the selected profile, not a hardcoded `8765`

## TLS Findings

Treat public `grpcs` as a separate topology requiring its own runbook, rehearsal, certificates, and rollback plan.

Important findings to verify on the deployed version:

- The default `initialize_local_ydb` entrypoint may not bring up a usable `grpcs` listener for every topology.
- A manual `/ydbd server ... --grpcs-port ...` startup path may be required in rehearsals.
- YDB discovery can fall back to `FQDNHostName()` when public host and public SSL port are not set, causing internal Docker hostnames to be advertised and TLS hostname validation to fail.
- Explicit public host and public gRPCs port may be needed to avoid discovery mismatches.

## Pitfalls

- `security_config.default_users` is bootstrap-oriented; existing volumes need explicit user verification or creation.
- Empty viewer, monitoring, or admin SID lists can be too permissive depending on YDB config semantics. Fill them deliberately.
- Dynamic-node registration can break if `register_dynamic_node_allowed_sids` does not include the SID used by the node registration path.
- In an auth-enabled deployment, a new dynamic node can register successfully and still fail its later config/bootstrap fetch. `Access denied without user token` means no suitable token reached the config fetch path. `Cannot get node config. Access denied. Node is not authorized` means a token reached the path but its SID is not allowed.
- Do not assume `--user root --password-file ...` or a global `--token-file` on `ydbd server` authorizes dynamic config fetch. Validate the current server behavior.
- Do not write `StaffApiUserToken` unquoted or as a raw token file. Generate text protobuf with quoted string values and inspect a redacted copy if parsing fails.
- Do not treat a registered node ID as proof that the node is usable; verify logs, `nodelist`, tenant metadata, and client health.
- When a dynamic-node attempt fails in a restart loop, prefer `docker update --restart=no <name>` followed by `docker stop <name>` to preserve logs. Do not remove working or newly registered containers until the replacement node is healthy.
- On `ghcr.io/ydb-platform/local-ydb:26.1.1.6`, a dynamic node can successfully register and still crash if it reuses a config file containing `grpc_config.ca/cert/key=/ydb_certs/...` without those files mounted. Sanitize the dynamic-node copy of the config or mount matching cert files.
- `YDB_ANONYMOUS_CREDENTIALS=1` in the static-node environment does not override `security_config.enforce_user_token_requirement: true`, but it is still confusing in docs. Explain the interaction if it remains present.
- Do not expose plaintext YDB gRPC publicly as a convenience shortcut.
