---
name: planetscale-cli-skills
description: PlanetScale CLI command reference and workflows. Use for authentication; org, SSO, teams, and billing; databases, branches, Neki, internal or external keyspaces, keyspace parameters, logs, maintenance, extensions, metrics, insights, inspect, and SQL; deploy requests, schema migrations, MoveTables, throttlers, rollout concurrency, disk-storage settings, and Traffic Control; PgBouncers, dedicated read replicas, roles, passwords, backups, webhooks, audit logs, service tokens, D1 imports, and automation. Routes to focused pscale sub-skills. Triggers on PlanetScale CLI, pscale, pscale --skill, database, branch, Neki, Neki read-only replicas, --read-only-replicas, keyspace, keyspace parameters, create-external, external keyspace, deploy request, move-tables, vtctl, vtctld, max rollout, disk scaling, max storage, throttler, traffic-control, metrics, insights, inspect, SQL, role, password, pgbouncer, dedicated read replica, read-only replica, backup, webhook, audit-log, billing, org, SSO, service token, import d1.
requirements:
  binaries:
    - pscale
    - jq
  env_optional:
    - PLANETSCALE_SERVICE_TOKEN_ID
    - PLANETSCALE_SERVICE_TOKEN
  notes: |
    Requires PlanetScale CLI authentication via 'pscale auth login' or approved service tokens; the CLI manages credential persistence.
    Automation scripts use jq for structure-aware parsing of pscale JSON output.
metadata:
  openclaw:
    purpose: >
      Provide command reference and automation for PlanetScale CLI (pscale) operations only.
      Scope is limited to: database and branch management, Neki operational management, logs, maintenance schedule inspection and Postgres window/event management, dedicated PostgreSQL PgBouncers and read replicas, Postgres Traffic Control, VTGate sizing, Vitess keyspace parameters and read-only-region access, webhook management, billing inspection/payment-method management, deploy requests,
      non-interactive SQL queries, historical/current performance metrics, query insights, read-only diagnostics, Cloudflare D1 imports, backups, audit-log exports, passwords,
      authentication-attempt exports, service tokens, and organization management via the pscale CLI tool.
    capabilities:
      - Run pscale CLI commands to manage PlanetScale databases, branches, Neki resources, branch logs, maintenance schedule inspection and Postgres window/event management, keyspace parameters, dedicated PgBouncers, PostgreSQL dedicated read replicas, webhooks, Postgres Traffic Control, billing, deploy requests, D1 imports, non-interactive SQL queries, performance metrics, query insights, read-only diagnostics, audit-log exports, and authentication-attempt exports
      - Execute bundled automation scripts (create-branch-for-mr.sh, deploy-schema-change.sh, sync-branch-with-main.sh)
      - Read PlanetScale CLI output and help users interpret results
    install_mechanism: >
      Skill files are loaded into agent context when a matching PlanetScale/pscale task is detected.
      Automation scripts are executed directly via shell (bash). No network access beyond pscale CLI calls.
      Scripts do not use eval or dynamic code execution; all pscale arguments are passed as discrete tokens.
    requires:
      credentials:
        - name: PLANETSCALE_SERVICE_TOKEN_ID
          description: >
            PlanetScale service token ID for CI/CD authentication. Optional — interactive login
            via 'pscale auth login' can be used instead. The CLI consumes the configured credential;
            this skill does not read, store, or transmit credentials beyond passing them to pscale CLI.
          required: false
        - name: PLANETSCALE_SERVICE_TOKEN
          description: >
            PlanetScale service token secret for CI/CD authentication. Optional — interactive login
            via 'pscale auth login' can be used instead. The CLI consumes the configured credential;
            this skill does not read, store, or transmit credentials beyond passing them to pscale CLI.
          required: false
---

# PlanetScale CLI Skills

Comprehensive `pscale` command reference and workflows for managing PlanetScale databases via terminal.

## Destructive-operation safety

These gates apply to every destructive example here, including deletion, demotion, protection removal, connection/transaction termination, deploy-request closure/revert, and cleanup. Command examples and CLI confirmation prompts are not authorization.

1. Inspect fresh state and confirm support for the target engine and installed CLI. Obtain explicit approval for the exact organization and, where applicable, database, branch, and resource ID/name, plus the operation and flags; use an explicit `--org` on every operation. Stop on unsupported operations or uncertain identity.
2. Check dependencies and availability: applications, active users, child resources, routing, pending changes, and the maintenance window. Do not infer that a stale, merged, or unused-looking resource is disposable.
3. Require a verified recovery path that survives the operation: confirm backup/export usability and retention, or tested replacement/recreation instructions, ownership, and recovery time. A backup name alone is not verification; stop if recovery cannot be established.
4. Execute only the approved action. Force flags, descendant deletion, demotion, and disabling protection require separate explicit approval; never add them to work around a refusal. For a known headless session, obtain approval for the required force flag up front, before attempting the operation; stop if that approval is absent or any attempt is refused.
5. Perform read-back verification of the exact target and dependent service health. Inspect pending/asynchronous outcomes before claiming completion. Authentication/network errors are not proof of absence; an ambiguous result requires investigation, not an automatic retry.

## Overview

The PlanetScale CLI brings database branches, deploy requests, and schema migrations to your fingertips. This skill provides command references, automation scripts, and decision trees for the covered `pscale` workflows. Confirm installed-command and engine support before acting.

## Configuration and credential safety

- Directory-local `.pscale.yml` files are project configuration, not trusted credential configuration. The CLI accepts only `org`, `database`, and `branch` from them and warns while ignoring keys such as API endpoints or tokens.
- Keep API URLs and credentials in the user config, environment/secret manager, or explicit approved flags. Never commit them to a repository-local config.
- `pscale api` follows cross-host redirects without forwarding authentication or caller-supplied headers. Even with this protection, pass secret-bearing headers only to an explicitly verified API host and do not expose them in logs.
- When `--format json` is active, raw API error codes are preserved in `issues[0].code` instead of being collapsed to `COMMAND_FAILED`. Branch automation should branch on that exact nested code when present.
- `schema_mutation_blocked`, `schema_refreshing`, and `schema_snapshot_not_ready` responses use `status: "action_required"` and one CLI-generated `next_steps` instruction. Treat them as retryable waits, not hard failures or permission to retry blindly: wait for the active vtctld mutation or deploy to finish, or for the branch schema snapshot to become ready, then re-read state before retrying.
- A Postgres `resize in progress` error also yields `status: "action_required"` with wait/status guidance. Inspect `pscale branch resize status`, wait for the existing change to finish, and re-read the intended state before retrying; do not re-authenticate or cancel another operator's change as a shortcut.
- Route MySQL/Vitess schema snapshot refresh/readiness to `pscale-branch`: `refresh-schema` waits for `schema_ready` with 2-second polling and a 2-minute readiness bound. On `schema_refreshing` or `schema_snapshot_not_ready`, read back readiness before retrying the follow-up reader; preserve poll failures rather than treating every error as a snapshot timeout.
- Route single-request `create/update --aggressive-cutover` to `pscale-deploy-request`. It can kill blockers on the first cutover attempt and requires explicit approval plus read-back; database defaults and emergency `force-cutover` are separate actions.
- Route parameter update-requirement interpretation to `pscale-branch` for Postgres catalogs and `pscale-neki` for configuration-profile, sidecar, and admin catalogs. `REQUIRES UPDATE` is a human boolean indicator; JSON `requires_update` preserves a nullable string. Inspect non-null requirements before proposing writes; they do not authorize automatic maintenance or capacity changes.
- Route Postgres branch extension enable/disable and Vitess VTGate parameter/update/change-rollout work to `pscale-branch`. Route approved failed deploy-operation retries to `pscale-deploy-request`; retry is not queue unblocking or revert. Keyspace storage size units and staff-managed maximum limits belong to `pscale-database`.
- Route Neki read-only replica capacity to `pscale-neki` and `branch config-profile create/update --read-only-replicas`. These per-shard counts are not dedicated PostgreSQL replica resources; confirm the engine and retain exact-target capacity/cost approval.
- Route Neki live router sessions to `pscale-branch` (`branch connections show/top` plus separately approved termination): use fresh matching action IDs, respect permissions, omit engine-incompatible flags, and preserve incomplete-result warnings. Live `top` controls do not establish authorization; replay remains read-only. Sidecar settings belong to `pscale-neki` and `config-profile update --parameters sidecar.<name>=<value>`; `branch sidecar` is deprecated. Parameter inventories expose `INTERNAL` / JSON `internal`; internal settings are not write candidates, and false alone is not authorization.

## Binary-native agent bootstrap

- `pscale --skill` prints the current binary's installable `pscale-cli` skill file to stdout when no positional arguments follow it. `pscale agent-guide --skill` is equivalent.
- Both forms still emit the raw Markdown skill when `--format json` is present; redirect the output to an approved skills directory when a standalone binary-native guide is wanted.
- Validate automated bootstrap output starts with `---\nname: pscale-cli`; do not infer a valid skill document from exit status alone.
- The binary-native guide is useful for first-party command discovery, but it does not replace this repository's specialized safety workflows, focused references, and helper scripts.
- Unrecognized root tokens and subcommands of non-runnable command groups fail with exit status 2 instead of printing help and exiting zero. Runnable groups such as `keyspace parameters` can interpret an unrecognized token as a positional argument and execute their default action, so automation must validate the expected JSON/resource shape as well as the exit code.
- For unknown non-runnable subcommands, the error points to the owning parent's `--help`; JSON `UNKNOWN_COMMAND` next steps also name that parent (for example, `pscale role --help`). Inspect that read-only help to correct the command, not the root inventory alone. Suggestions are not authorization to execute an operational command. The `show` aliases for role, Neki data-topology, and MySQL routing-rules lookups are documented in their focused references.
- The top-level `pscale data-imports` family is unavailable. Use `pscale keyspace create-external` to attach an external MySQL source and `pscale branch vtctl move-tables` for table-movement workflows; treat an unknown-command error as a failed operation.

## Sub-Skills

| Command | Skill | Use When |
|---------|-------|----------|
| **auth** | `pscale-auth` | Login, logout, service tokens, authentication management |
| **branch/logs** | `pscale-branch` | Create, restore to a PostgreSQL recovery point, rename, protect, delete, promote, diff, list, and switchover branches; refresh MySQL schema snapshots and verify readiness; query PostgreSQL/Neki branch logs; inspect branch infra, manage Postgres size/replicas/parameters/maintenance/extensions, toggle Postgres extensions, run Postgres/Neki branch maintenance, resize Vitess VTGates and roll out VTGate parameter changes, manage live keyspace routing rules, Lookup Vindexes, and tablet throttling, manage query pattern reports, manage Vitess MoveTables workflows |
| **deploy-request** | `pscale-deploy-request` | Create, review, inspect queues/operations, check storage, throttle, deploy, update auto-apply/auto-delete/per-request aggressive-cutover settings, retry failed operations after diagnosis, unblock failed deploy/revert queues, force cutover, and revert schema changes |
| **database** | `pscale-database` | Create, list, show, update, delete, and dump databases; manage database-level and keyspace-level Vitess throttlers, keyspace VTTablet/MySQL parameters, rollout concurrency, disk-storage settings, internal/external keyspaces, aggressive-cutover defaults, PostgreSQL IP restrictions, and read-only regions |
| **neki** | `pscale-neki` | Manage Neki data topology, shards, branch-wide change requests, config profiles, per-shard read-only replica capacity (`--read-only-replicas`) and extension sets, routers, sidecars, admin config, profile maintenance, restore sizing overrides, target-specific inspection, and router/shard role access |
| **maintenance** | `pscale-maintenance` | Inspect Vitess Enterprise schedules/history and Postgres branch windows/events; approve exact-target window changes or event rescheduling with deadline and recovery checks |
| **sql** | `pscale-sql` | Run non-interactive SQL queries with JSON output and ephemeral credentials |
| **metrics** | `pscale-metrics` | Query historical/current branch metrics and engine-aware grouped performance reports |
| **insights** | `pscale-insights` | Analyze production query statistics, execution samples, query tags, error details, anomaly correlations, and schema recommendations |
| **traffic-control** | `pscale-traffic-control` | Inventory and safely manage Postgres Traffic Control budgets and fingerprint/keyspace/tag rules |
| **inspect** | `pscale-inspect` | Run point-in-time, read-only MySQL/Vitess, PostgreSQL, and Neki diagnostic checks against one connection target |
| **import d1** | `pscale-import-d1` | Import Cloudflare D1 SQLite exports into PlanetScale Postgres |
| **backup** | `pscale-backup` | Create, list, show, restore, and delete branch backups; approve emergency live-tablet sources and manage scheduled backup policies |
| **billing** | `pscale-billing` | Inspect invoices and manage organization payment methods with sensitive billing-data safeguards |
| **audit-log** | `pscale-audit-log` | List audit events and export filtered authentication attempts |
| **password** | `pscale-password` | Create, list, show, update, delete, and scope Vitess connection passwords to read-only regions; inspect and mutate Postgres/Neki roles, inherited-role pairings, and connection targets |
| **pgbouncer** | `pscale-pgbouncer` | List, inspect, create, resize, cancel, and delete dedicated PostgreSQL PgBouncers |
| **dedicated-read-replica** | `pscale-read-only-replica` | List, inspect, create, resize, configure, detach with irreversible-operation approval, and delete dedicated PostgreSQL read replicas; recognize the deprecated `read-only-replica` compatibility name |
| **webhook** | `pscale-webhook` | List, inspect, create, update, test, and delete database webhooks, including authorization headers |
| **org** | `pscale-org` | List, show, switch, and update organizations; manage SSO, directory sync, email domains, members, and teams |
| **service-token** | `pscale-service-token` | Create, show, and manage CI/CD service tokens; inspect nullable last-used IP/network metadata |

Route Postgres scheduled maintenance to `pscale-maintenance` (`branch maintenance window/event`); immediate Postgres/Neki maintenance stays in `pscale-branch`. Promotion/demotion sizing belongs to `pscale-branch`, requires engine/feature and capacity approval, and does not support Neki. Detach belongs to `pscale-read-only-replica`, is hidden/feature-gated, and is never automatic cleanup.

## Decision Trees

### Should I use a branch or deploy request?

```
What's your goal?
├─ Experimenting with schema changes → Create branch (pscale-branch)
├─ Testing schema in isolation → Create branch (pscale-branch)
├─ Ready to deploy schema to production → Create deploy request (pscale-deploy-request)
└─ Reviewing schema changes before production → Review deploy request (pscale-deploy-request)
```

### Service token vs password?

```
What's your use case?
├─ CI/CD pipeline → Service token (pscale-service-token)
├─ Local development → Password (pscale-password)
├─ Production application → Service token (rotatable, secure)
└─ One-off admin task → Password (temporary)
```

### Schema deployment or lifecycle/capacity change?

```
What's your goal?
├─ Deploy schema changes → Deploy-request review/approval workflow (pscale-deploy-request)
├─ Promote branch lifecycle/capacity → Engine, capacity, recovery and approval gates (pscale-branch)
└─ Experiment with schema → Isolated development branch, not a promotion shortcut
```

Promotion does not deploy another branch's schema; it is not an alternative to a deploy request.

## Common Workflows

### Schema Migration Workflow

Complete workflow from branch creation to production deployment:

```bash
# 1. Create development branch
pscale branch create <database> <branch-name>

# 2. Make schema changes (via shell, ORM, or direct SQL)
pscale shell <database> <branch-name>

# 3. View schema diff
pscale branch diff <database> <branch-name>

# 4. Create deploy request
pscale deploy-request create <database> <branch-name>

# 5. Review and deploy
pscale deploy-request deploy <database> <deploy-request-number>

# 6. Verify deployment
pscale deploy-request show <database> <deploy-request-number>
```

See `scripts/` directory for automation.

### Branch Development Workflow

```bash
# Create branch from main
pscale branch create <database> <feature-branch> --from main

# Work on schema changes
pscale shell <database> <feature-branch>

# Check diff before deploying
pscale branch diff <database> <feature-branch>

# Create deploy request when ready
pscale deploy-request create <database> <feature-branch>
```

### CI/CD Integration

```bash
# Create service token for CI/CD
pscale service-token create --org <org>

# Use in CI/CD pipelines (GitHub Actions, GitLab CI, etc.)
export PLANETSCALE_SERVICE_TOKEN_ID=<token-id>
export PLANETSCALE_SERVICE_TOKEN=<token>

# Create and deploy via CI/CD after review/approval gates pass
pscale deploy-request create <database> <branch> --format json
pscale deploy-request deploy <database> <deploy-request-number>
```

### Cloudflare D1 to PlanetScale Postgres import

```bash
# Lint and dry-run first; review the JSON migration ID and warnings
pscale import d1 lint --input ./d1-export.sql --format json
pscale import d1 start <database> <branch> --input ./d1-export.sql --dry-run --format json

# After explicit confirmation, run and verify the import
pscale import d1 start <database> <branch> --input ./d1-export.sql --migration-id <id> --format json
pscale import d1 verify <database> <branch> --migration-id <id> --input ./d1-export.sql --format json
```

## Quick Reference

### Most Common Commands

```bash
# Authentication
pscale auth login
pscale auth logout

# Branch management; deletion requires the destructive-operation safety gates
pscale branch create <database> <branch> [--from <source-branch>]
pscale branch list <database>
pscale branch delete <database> <branch> --org <org>
pscale branch parameters list <database> <branch> --format json
pscale branch resize status <database> <branch> --format json
pscale branch vtgate show <database> <branch> --format json
pscale branch update <database> <branch> --deletion-protected=true --format json

# Discover and use a Vitess read-only region
pscale keyspace read-only-regions <database> <branch> <keyspace> --format json
pscale keyspace read-only-regions add <database> <branch> <keyspace> <region> --cluster-size <size> --replicas <count>
pscale password create <database> <branch> <name> --read-only-region <region> --format json

# Deploy requests
pscale deploy-request create <database> <branch>
pscale deploy-request list <database>
pscale deploy-request storage-check <database> <number> --format json
pscale deploy-request operations <database> <number> --format json
pscale deploy-request deploy <database> <number>

# Dedicated PostgreSQL PgBouncers
pscale pgbouncer list <database> <branch> --format json
pscale pgbouncer show <database> <branch> <name> --format json

# Dedicated PostgreSQL read replicas
pscale dedicated-read-replica list <database> <branch> --org <org> --format json
pscale dedicated-read-replica show <database> <branch> <name> --org <org> --format json

# Database operations
pscale database create <database> --org <org>
pscale database list
pscale database show <database> --format json
pscale database ip-restriction list <database> --format json
pscale database throttler show <database> --org <org> --format json
pscale database aggressive-cutover show <database> --org <org> --format json
pscale keyspace settings <database> <branch> <keyspace> --org <org> --format json
pscale keyspace parameters list <database> <branch> <keyspace> --org <org> --format json
pscale shell <database> <branch>
pscale logs <database> <branch> --org <org> --format json

# Database webhooks
# Webhook resource JSON may include the signing secret; redact before capture.
set -o pipefail
pscale webhook list <database> --org <org> --format json |
  jq 'map(del(.secret))'
# Use `show` only when intentionally retrieving the secret; otherwise use the redacted sub-skill workflow.

# Maintenance schedules and windows (Vitess Enterprise)
pscale maintenance list <database> --org <org> --format json
pscale maintenance windows <database> <schedule-id> --org <org> --format json

# Backup policies and authentication-attempt exports
pscale backup policy list <database> --format json
pscale audit-log auth-attempts download --org <org> --since 24h --outcome deny

# Non-interactive read query for agents/scripts
pscale sql <database> <branch> --org <org> --format json --query "SELECT 1"

# Point-in-time diagnostics, branch metrics, and query-fingerprint analysis
pscale inspect all <database> <branch> --org <org> --format json
# Neki: pin one shard on the primary path by default
pscale inspect all <database> <branch> --org <org> --shard <shard-id> --format json
# Add --router <router> and/or --replica only for that explicit target path
pscale metrics report <database> <branch> --org <org> --period 1d --format json
pscale metrics show <database> <branch> --org <org> --metric queries --metric latency_p99 --period 1h --format json
pscale insights queries <database> <branch> --org <org> --sort p99Latency --period 1h --format json
pscale insights queries samples <database> <branch> <fingerprint> --org <org> --keyspace <keyspace> --format json
pscale insights tags summaries <database> <branch> --org <org> --tags app --sort totalTime --format json
pscale insights errors show <database> <branch> <full-error-fingerprint> --org <org> --format json
pscale insights anomalies show <database> <branch> <anomaly-id> --org <org> --format json
pscale insights recommendations <database> --org <org> --format json
pscale insights recommendations show <database> <number> --org <org> --format json
pscale insights queries show <database> <branch> <query-id> --org <org> --format json
pscale insights queries summary <database> <branch> <fingerprint> --org <org> --keyspace <keyspace> --format json

# Postgres Traffic Control inventory
pscale traffic-control budget list <database> <branch> --org <org> --format json

# Organization billing inspection
pscale billing invoice list --org <org> --page 1 --per-page 25 --format json
pscale billing payment-method show --org <org> --format json

# Cloudflare D1 import dry-run
pscale import d1 start <database> <branch> --input ./d1-export.sql --dry-run --format json
```

## Related Skills

- **drizzle-kit** - ORM schema management and migrations
- **gitlab-cli-skills** - GitLab MR workflow integration
- **github** - GitHub PR and CI/CD integration

## Automation Scripts

See `scripts/` directory for token-efficient automation:

- `create-branch-for-mr.sh` - Create PlanetScale branch matching your MR/PR branch name
- `deploy-schema-change.sh` - Complete schema migration workflow
- `sync-branch-with-main.sh` - Create a replacement branch from main/base for conflict resolution

Scripts execute without loading into context (~90% token savings).

## Resources

- Official docs: https://planetscale.com/docs/reference/planetscale-cli
- GitHub: https://github.com/planetscale/cli
- Community: https://github.com/planetscale/discussion
