---
name: pscale-password
description: Create, list, show, update, renew, and delete branch connection passwords, and manage Postgres/Neki roles and their connection targets. Use when creating connection strings, managing database credentials, routing Vitess reads, creating Neki viewer/operator roles, retrieving role details for Neki shard/router/replica paths or Postgres dedicated read replicas/PgBouncers, rotating credentials, updating password metadata, or filtering credentials. Triggers on password, connection string, database credentials, create password, show password, update password, CIDR, read-only region password, password status, Postgres role, Neki role, inherited roles, role create, role get, role status, role expiration, default Postgres role, Neki router, Neki shard, dedicated read replica, read-only replica, replica name, PgBouncer connection.
---

# pscale password

Create, list, filter, renew, and delete branch passwords for database connections. The `pscale password` command group is for Vitess databases; use `pscale role` for Postgres and Neki branch credentials.

## Destructive-operation safety

These gates apply to every destructive example here, including deletion, demotion, protection removal, connection/transaction termination, deploy-request closure/revert, and cleanup. Command examples and CLI confirmation prompts are not authorization.

1. Inspect fresh state and confirm support for the target engine and installed CLI. Obtain explicit approval for the exact organization and, where applicable, database, branch, and resource ID/name, plus the operation and flags; use an explicit `--org` on every operation. Stop on unsupported operations or uncertain identity.
2. Check dependencies and availability: applications, active users, child resources, routing, pending changes, and the maintenance window. Do not infer that a stale, merged, or unused-looking resource is disposable.
3. Require a verified recovery path that survives the operation: confirm backup/export usability and retention, or tested replacement/recreation instructions, ownership, and recovery time. A backup name alone is not verification; stop if recovery cannot be established.
4. Execute only the approved action. Force flags, descendant deletion, demotion, and disabling protection require separate explicit approval; never add them to work around a refusal. For a known headless session, obtain approval for the required force flag up front, before attempting the operation; stop if that approval is absent or any attempt is refused.
5. Perform read-back verification of the exact target and dependent service health. Inspect pending/asynchronous outcomes before claiming completion. Authentication/network errors are not proof of absence; an ambiguous result requires investigation, not an automatic retry.

## Common Commands

```bash
# Create password
pscale password create <database> <branch> <password-name>

# Create a reader password scoped to one separate Vitess read-only region
pscale keyspace read-only-regions <database> <branch> <keyspace> --format json
pscale password create <database> <branch> <password-name> \
  --read-only-region <region> \
  --format json

# List the default page (up to 100 passwords); omit branch to audit all branches
pscale password list <database> [branch]

# Audit renewable passwords across all branches
pscale password list <database> --status renewable --format json

# Filter and paginate passwords
pscale password list <database> <branch> \
  --name production \
  --status active \
  --page 1 \
  --per-page 100 \
  --format json

# Renew password
pscale password renew <database> <branch> <password-id>

# Show password metadata by ID or exact name
pscale password show <database> <branch> <password-id> --format json
pscale password show <database> <branch> --name production-app --format json

# Update password metadata or CIDR restrictions without rotating the secret
pscale password update <database> <branch> <password-id> --new-name production-app-v2 --format json
pscale password update <database> <branch> --name production-app --cidrs 10.0.0.0/8,192.168.1.1/32 --format json

# Delete password
pscale password delete <database> <branch> <password-id> --org <org>
```

`--name` performs a substring match. Password status values are `active`, `renewable`, and `expired`. List output is limited to one page by default; request subsequent pages with `--page` when needed.

When `--read-only-region` is present, the default role is `reader`, the created password is labeled as a read-only-region credential, and `--replica` is rejected. Use the region slug, display name, or ID returned by `pscale keyspace read-only-regions`. The plaintext secret is shown only at creation time: capture it directly into an approved secret manager and never print it in logs or commit it.

### Show or update Vitess password metadata

`pscale password show` returns metadata only. The secret cannot be retrieved after create or renew. `show`, `update`, and `delete` can identify a password by ID or by `--name`; use IDs when names are ambiguous.

```bash
# Inspect metadata before changing it
pscale password show <database> <branch> <password-id> --org <org> --format json
pscale password show <database> <branch> --org <org> --name <password-name> --format json

# Change the display name without rotating the password
pscale password update <database> <branch> <password-id> --org <org> \
  --new-name <new-name> \
  --format json

# Replace CIDR restrictions; pass an empty value to clear all restrictions
pscale password update <database> <branch> --org <org> \
  --name <password-name> \
  --cidrs 10.0.0.0/8,192.168.1.1/32 \
  --format json
pscale password update <database> <branch> --org <org> \
  --name <password-name> \
  --cidrs "" \
  --format json

# Verify the metadata after the write
pscale password show <database> <branch> <password-id> --org <org> --format json
```

Updating a name or CIDR allowlist does not rotate the secret. Treat updates as credential-access writes: show the target password metadata, exact new name/CIDRs, and clearing behavior before asking for approval, then verify with `show` or `list`. Use create/delete or `renew` only when the user needs a new secret.

## Workflows

### Application Connection

```bash
# Create password for production app
pscale password create my-database main production-app

# Returns connection string:
# mysql://username:password@host/database

# Use in application environment variables
export DATABASE_URL="mysql://..."
```

### Local Development

```bash
# Create temporary password for local dev
pscale password create my-db main local-dev

# Review cleanup under the safety gates; verify dependencies and obtain approval
pscale password delete my-db main <password-id> --org <org>
```

### Region-scoped read access

```bash
# Discover configured regions and confirm the intended target is ready
pscale keyspace read-only-regions <database> <branch> <keyspace> \
  --org <org> --format json

# Create a temporary, reader-only credential for that region
pscale password create <database> <branch> reporting-reader \
  --org <org> \
  --read-only-region <region> \
  --role reader \
  --ttl 24h \
  --format json
```

Use `--read-only-region` when reads must stay in one separate region. Use `--replica` instead when reads may route to the primary region's replicas and all read-only regions. The two routing modes are mutually exclusive.

### Postgres and Neki role creation, lookup, and filtering

Postgres and Neki databases use roles instead of Vitess branch passwords. `pscale role default` is a read-only lookup for the default `postgres` role and does not rotate credentials. Use `pscale role reset-default` only when the user explicitly asks to reset default-role credentials and approves the connection impact. Role list/get/default output includes `status` and `expires_at`; listing supports pagination and name filtering plus status filters for `active`, `renewable`, `disabled`, and `expired`.

This workflow intentionally lives here because no dedicated `pscale-role` skill exists, and both command groups manage branch credentials.

`pscale role show` is an alias of `role get` with identical arguments, target selectors, output, and secret-handling rules; use canonical `get` in new automation. Before using the alias or relying on generated URL parameters, check `pscale version` against the [installed CLI compatibility notes](references/commands.md#pscale-role-get); an older URL without `sslrootcert` is not by itself malformed. If the installed CLI rejects an unknown role subcommand, inspect `pscale role --help` as directed by the human error or JSON `UNKNOWN_COMMAND` next step. Do not automatically execute suggested operational actions.

Role `database_url` output uses `sslmode=verify-full&sslrootcert=system`, including Postgres/Neki role lookups and newly created or reset role credentials. Libpq 16+ interprets `system` as the SSL implementation's trusted CA roots rather than its default `~/.postgresql/root.crt`; support in non-libpq drivers depends on the driver and version. Check the actual consumer before reusing a URL. For any consumer that does not support `sslrootcert=system` (including older libpq or non-libpq drivers that treat it as a filename), retain `sslmode=verify-full` and substitute an explicit approved trusted CA-bundle path, or upgrade to a consumer with verified support. Never disable certificate or hostname verification or drop TLS parameters merely to make the connection work. See the [client compatibility and source details](references/commands.md#pscale-role-get). A lookup is not authorization to rotate a role or expose its returned URL.

If `role default` receives `NOT_FOUND` and a separate branch lookup succeeds, the CLI distinguishes **default credentials not yet created** from a missing database or branch. With `--format json`, it emits `status: "action_required"`, an `issues` entry with `code: "NOT_FOUND"`, and proposed `next_steps` to stdout, then exits with status 1. Exit 1 identifies action-required handling, while generic fatal errors use exit 2; exit 1 alone does not identify which action is needed. Preserve and parse stdout `status` and `issues` even on nonzero exit, rather than relying on the exit code or stderr alone to identify this condition. Invalid or missing JSON is not evidence that credentials need creation.

Without JSON format, the plain error directly suggests `pscale role reset-default <database> <branch>` without `--org`, `--force`, or approval wording. Treat both this human-format instruction and JSON `next_steps` as proposals, never authorization. Inspect the exact org/database/branch and ask for explicit approval to create default credentials before using `role reset-default`; pass explicit `--org <org>` instead of relying on the configured default. If credentials already exist, resetting rotates them and can break existing connections. Never automatically execute either suggested command or add `--force`, and never expose the returned password or connection URL. If branch lookup also fails, investigate the original not-found/permissions condition rather than assuming credentials need creation.

```bash
pscale role list <database> <branch> \
  --name production \
  --status active \
  --page 1 \
  --per-page 100 \
  --format json
pscale role default <database> <branch> --format json

# Create Neki roles only after confirming the intended privilege pairing
pscale role create <database> <branch> viewer --org <org> --format json \
  --inherited-roles neki_viewer,pg_read_all_data
pscale role create <database> <branch> operator --org <org> --format json \
  --inherited-roles neki_operator,postgres

# Postgres alternate connection targets
pscale role get <database> <branch> <role-id> --org <org> --format json --replica
pscale role get <database> <branch> <role-id> --org <org> --format json --dedicated-read-replica <replica-name>
pscale role get <database> <branch> <role-id> --org <org> --format json --bouncer <bouncer-name>

# Neki target selectors can be combined
pscale role get <database> <branch> <role-id> --org <org> --format json \
  --shard <shard-name> --router <router-name> --replica
```

Neki `--inherited-roles` supports `neki_viewer` only with `pg_read_all_data`, and `neki_operator` only with `postgres`; the API rejects an incomplete pairing. Role creation returns a credential, so obtain approval for the exact role name and privilege set, then capture the secret directly into an approved secret manager.

`--replica`, `--dedicated-read-replica`, and `--bouncer` are mutually exclusive. Named `--dedicated-read-replica` and `--bouncer` targets are Postgres-only and cannot combine with Neki `--router` or `--shard`. `--dedicated-read-replica` takes the replica **name** returned by branch infrastructure or `pscale dedicated-read-replica list`, not a read-only-region slug. The hidden deprecated `--read-only-replica` flag remains a compatibility alias, but new automation should use the canonical flag. A targeted response can change `username`, `access_host_url`, and `database_url`; PgBouncer URLs use port `6432`.

On Neki, `--replica`, `--router`, and `--shard` can be combined: router selection rewrites the username, while replica and shard selection produce libpq `options` and an options-bearing `database_url`. Use the shard **name** from `pscale branch shard list`, not its API ID; `pscale inspect --shard` is different and takes the ID.

A target-specific `NOT_FOUND` can mean the role or any requested target was not found, so verify every identifier before retrying. Treat returned passwords, connection URLs, and libpq options as secrets: capture them directly into an approved secret manager and never print them in logs or commit them.

## Troubleshooting

### Password not working

**Solution:** Inspect status and metadata first. For ordinary name or CIDR allowlist changes, use `password update`; delete/recreate or renew only when the secret itself has expired or must rotate.

```bash
pscale password list <database> <branch> --format json
pscale password show <database> <branch> <password-id> --format json
# After explicit approval; --cidrs replaces the entire allowlist
pscale password update <database> <branch> <password-id> --cidrs <cidr-allowlist> --format json
```

## Related Skills

- **pscale-service-token** - For CI/CD authentication (preferred over passwords)
- **pscale-database** - Database management

## References

See `references/commands.md` for complete command reference.
