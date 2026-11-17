# MCP Tool Scenarios

Concrete scenarios for testing every `local-ydb` MCP tool in this repository.

These scenarios are intentionally opinionated and reflect what actually worked in this repo during local runs.

## Scope

This document covers all public `local_ydb_*` tools currently registered by the MCP server:

- `local_ydb_inventory`
- `local_ydb_database_status`
- `local_ydb_healthcheck`
- `local_ydb_container_logs`
- `local_ydb_destroy_stack`
- `local_ydb_status_report`
- `local_ydb_tenant_check`
- `local_ydb_scheme`
- `local_ydb_generate_schema`
- `local_ydb_apply_schema`
- `local_ydb_sql`
- `local_ydb_permissions`
- `local_ydb_nodes_check`
- `local_ydb_graphshard_check`
- `local_ydb_auth_check`
- `local_ydb_storage_placement`
- `local_ydb_add_storage_groups`
- `local_ydb_reduce_storage_groups`
- `local_ydb_storage_leftovers`
- `local_ydb_list_versions`
- `local_ydb_pull_image`
- `local_ydb_pull_status`
- `local_ydb_bootstrap_root_database`
- `local_ydb_bootstrap`
- `local_ydb_create_tenant`
- `local_ydb_start_dynamic_node`
- `local_ydb_add_dynamic_nodes`
- `local_ydb_remove_dynamic_nodes`
- `local_ydb_restart_stack`
- `local_ydb_upgrade_version`
- `local_ydb_list_dumps`
- `local_ydb_dump_tenant`
- `local_ydb_restore_tenant`
- `local_ydb_prepare_auth_config`
- `local_ydb_write_dynamic_auth_config`
- `local_ydb_apply_auth_hardening`
- `local_ydb_set_root_password`
- `local_ydb_cleanup_storage`

## Profiles

Use these profiles from `examples/local-ydb.config.example.json`:

- `ghcr261-clean`: isolated clean stack on `ghcr.io/ydb-platform/local-ydb:26.1.1.6`
- `ghcr261-auth`: same stack, but with auth artifacts enabled
- `local`: auth-enabled working stack on the default ports

Treat `ghcr-rebuild-clean` and `ghcr-rebuild-auth` as historical rehearsal profiles. Prefer the `ghcr261-*` pair for current testing.

## Global Rules

- Run `local_ydb_check_prerequisites` first on a new host or profile.
- If `local_ydb_check_prerequisites` reports installable packages, review its plan-only output and then use `confirm: true` to install supported host helpers before trying deeper checks.
- Run read-only tools first.
- Use `local_ydb_list_versions` before `local_ydb_upgrade_version` when you need to verify the exact registry tag to deploy.
- If an image is not already present on the target host, use `local_ydb_pull_image(confirm=true)` and poll `local_ydb_pull_status` before bootstrap or upgrade.
- For mutating tools, call plan-only once before `confirm: true` unless you are deliberately smoke-testing an idempotent path.
- Do not test `cleanup_storage` against active volumes or paths.
- Do not mix static and dynamic image tags inside one profile.
- For stable GHCR tests, use the exact patch tag `ghcr.io/ydb-platform/local-ydb:26.1.1.6`.

<!-- BEGIN DECLARATIVE TOPOLOGY CONTRACT -->
## Declarative Topology Contract

- `dynamicNodeCount` is the total configured tenant-node count, including primary, and defaults to `1`.
- Configured node `1` uses `dynamicContainer`; nodes `2..N` use `dynamicContainer-<index>` and base ports plus `index - 1`.
- Configured dynamic names must be distinct from the static container; bootstrap, add, and standalone primary start validate names and the complete shared-network port set before returning a plan.
- Static IC port `19001` is reserved; all configured and one-off ports share the static node's network namespace and must not collide with it.
- The static container publishes the static gRPC port and every configured dynamic gRPC port on loopback. One-off nodes do not change those bindings.
- Tenant bootstrap recreates configured containers in index order, even when a stale container is already running. Readiness requires a stable running exact container plus IC registration; a matching nodelist port alone is insufficient.
- Default `local_ydb_add_dynamic_nodes` starts at `dynamicNodeCount + 1`; an explicit `startIndex` must be greater than `dynamicNodeCount`, and higher suffixes are one-off runtime nodes.
- Default `local_ydb_remove_dynamic_nodes` considers only suffixes above `dynamicNodeCount`; explicit selectors or `startIndex` can remove a configured suffix and create drift.
- Before any restart mutation, the existing static container must pass the full profile check, including exact configured loopback bindings. A mismatch leaves all container IDs and states unchanged and requires destroy/bootstrap.
- Restart unconditionally recreates every configured container, including containers observed restarting. It reports missing configured and unexpected one-off containers, never removes unexpected containers, and attempts to restore every preflight-running unexpected container even when restart fails.
- Restart rollback uses restart or bootstrap reconciliation because inventory does not retain removed configured container definitions.
- Removal rollback restores configured nodes through restart or bootstrap and recreates one-off nodes through add; a mixed selection returns both instructions.
- Auth hardening runs the full static compatibility preflight before any config or container mutation, then recreates and verifies every configured node in index order, including profiles without a dynamic-node token file; rollback also uses restart or bootstrap reconciliation.
- Partial primary starts and one-off additions repeat the full static compatibility preflight after checking image presence and immediately before every dynamic container launch. Each container is created but not started until its resolved immutable image ID matches the static container; a concurrent named-tag refresh removes the never-started container and fails closed before later nodes, while a preflight mismatch requires destroy followed by bootstrap.
- Storage reduction and version upgrade inspect and preserve exact one-off gRPC, monitoring, and IC ports before dump or destroy; an incomplete container definition aborts the rebuild before destructive work.
<!-- END DECLARATIVE TOPOLOGY CONTRACT -->

## Declarative Topology Acceptance Flow

Use only a disposable profile with unique container/network/volume names and non-overlapping contiguous port ranges. Keep cleanup in `finally`.

1. Bootstrap with `dynamicNodeCount: 1`. Save the static and primary container IDs, bindings, and running/stopped states.
2. Change the same profile to `dynamicNodeCount: 3`. Restart plan-only must place the full static compatibility check before every mutation. Confirmed restart must reject the missing configured bindings without changing saved IDs/states or creating `-2`/`-3`; tenant bootstrap must reject the same shared compatibility contract.
3. Confirm destroy, then perform a fresh count-3 bootstrap. Inventory must contain the primary, `-2`, and `-3`; the static container must publish exactly the static and all three configured dynamic gRPC ports on loopback; authenticated `nodelist` must contain all three derived IC ports; `scheme ls` through every configured dynamic gRPC endpoint and `local_ydb_tenant_check` must pass.
4. Call `local_ydb_add_dynamic_nodes` without `startIndex`. It must plan and create `-4`. Save its Docker ID and running state from inventory.
5. Remove configured container `-2` explicitly. Call restart plan-only and require `missingDynamicContainers=["<dynamicContainer>-2"]` and `unexpectedDynamicContainers=["<dynamicContainer>-4"]`. The plan must not contain `docker rm -f <dynamicContainer>-4`.
6. Replace configured `-2` with a same-name restart-looping fixture. Restart plan-only must contain an unconditional remove/run for `-2`; confirmed restart must give it a new Docker ID. The preflight-running `-4` must retain its saved Docker ID and running state. Exact configured IC ports and tenant metadata must pass again.
7. While `-4` exists with non-default gRPC, monitoring, and IC ports, plan a storage reduction or version upgrade rebuild. Only `-4` may appear in `extraDynamicNodes`; its exact inspected ports must be reused, while configured `-2` and `-3` come from bootstrap/auth reconciliation. Withhold one inspected port as a negative control and require failure before dump or destroy. Final container/image and nodelist verification must cover configured nodes plus `-4`.
8. Confirm destroy, then bootstrap again. Inventory must contain exactly the three configured dynamic containers and no `-4`.
9. In `finally`, destroy the disposable stack and independently remove any leftover disposable containers, network, and volume.

<!-- BEGIN MANAGED SQL SCENARIOS -->
## Managed SQL Scenario: Query Service Safety Matrix

Goal: exercise `local_ydb_sql` against the selected configured local-ydb profile. Use the official `ydb-mcp` server instead when the target is an arbitrary YDB endpoint rather than a toolkit-managed local-ydb profile.

Preparation:

- Create a disposable `managed_sql_smoke` table with `local_ydb_apply_schema`.
- Run every cleanup step from a `finally` block, including after an assertion or preflight failure.
- Never reuse a table that contains non-test data.
- For the authenticated Linux SSH fixture, keep static and dynamic gRPC ports unpublished, set `profile.network` to the static container's user-defined bridge, let the dynamic node share the static container namespace, and expose the root password file only as a read-only remote secret.

Calls:

```json
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "query", "script": "SELECT $value AS value;", "parameters": { "value": { "type": { "kind": "primitive", "name": "Int32" }, "value": 42 } } } }
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "query", "script": "UPSERT INTO `managed_sql_smoke` (id, value) VALUES (1, \"blocked\");", "confirm": true } }
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "query", "script": "SELECT COUNT(*) AS count FROM `managed_sql_smoke`;" } }
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "explain", "script": "SELECT id, value FROM `managed_sql_smoke`;" } }
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "execute", "script": "UPSERT INTO `managed_sql_smoke` (id, value) VALUES (1, \"confirmed\");" } }
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "execute", "script": "UPSERT INTO `managed_sql_smoke` (id, value) VALUES (1, \"confirmed\");", "confirm": true } }
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "execute", "script": "THIS IS NOT VALID YQL;", "confirm": true } }
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "explain", "script": "ALTER TABLE `managed_sql_smoke` ADD COLUMN note Utf8;" } }
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "explain", "script": "CREATE TABLE `managed_sql_ctas_explain` (PRIMARY KEY (id)) WITH (STORE = COLUMN) AS SELECT id, value FROM `managed_sql_smoke`;" } }
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "query", "script": "SELECT value FROM AS_TABLE($items) ORDER BY value;", "maxRows": 2, "maxOutputBytes": 65536, "parameters": { "items": { "type": { "kind": "list", "item": { "kind": "struct", "fields": [{ "name": "value", "type": { "kind": "primitive", "name": "Int32" } }] } }, "value": [{ "value": 0 }, { "value": 1 }, { "value": 2 }] } } } }
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "query", "script": "SELECT $large AS first; SELECT $large AS second;", "maxOutputBytes": 256, "parameters": { "large": { "type": { "kind": "primitive", "name": "Utf8" }, "value": "<replace with an actual string of at least 4096 characters>" } } } }
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "query", "script": "SELECT $text AS text;", "parameters": { "text": { "type": { "kind": "primitive", "name": "Utf8" }, "value": "\ud800" } } } }
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "query", "script": "SELECT $record;", "parameters": { "record": { "type": { "kind": "struct", "fields": [{ "name": "\ud800", "type": { "kind": "primitive", "name": "Utf8" } }] }, "value": { "\ud800": "value" } } } } }
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "query", "script": "SELECT \"\ud800\" AS text;" } }
{ "tool": "local_ydb_sql", "arguments": { "profile": "ghcr261-clean", "action": "query", "script": "SELECT $path AS path;", "parameters": { "path": { "type": { "kind": "primitive", "name": "Utf8" }, "value": "<replace with this profile's configured rootPasswordFile path>" } } } }
```

Expected:

- `query` uses SnapshotRO even when `confirm=true`; the attempted UPSERT fails and the following count remains zero.
- `explain` returns a plan or AST without side effects.
- `execute` always performs mandatory EXPLAIN first. Without `confirm=true` it returns `outcome=planned`; with confirmation it sends one NoTx execution and performs no retries.
- Invalid confirmed YQL is blocked by failed preflight with `executed=false` and `confirmationConsumed=false`.
- Parameter names are bare names, declarations are generated deterministically, and response metadata contains canonical parameter types with configured credential paths redacted but does not echo supplied parameter values. Selected result rows can still contain those values.
- `maxRows` truncates a result set only between complete rows; the first row-limit hit stops all further result capture (read-only execution cancels, confirmed `NoTx` drains). `maxOutputBytes` is shared across captured issues, plan/AST, metadata, and rows.
- The byte-limit call's placeholder is documentation only; replace it with an actual value of at least 4096 characters, or an equivalent fixture that reliably exceeds the 256-byte capture budget.
- All three lone-surrogate calls are rejected before Query Service execution: they probe an Utf8 parameter, a Struct field name, and the script itself. Replace the credential-path placeholder with the selected profile's exact configured path; the returned row string is `<redacted>`.
- Result rows are arrays aligned with `columns`; their strings, nested object keys, and column names/types undergo recursive redaction for configured credential paths, the loaded root password, and recognized credential assignments. Colliding redacted keys retain every value through deterministic numeric suffixes, and redaction expansion remains charged to `outputBytes`. Inspect `outcome`, truncation flags, and `outputBytes` rather than treating partial output as success.
- On an authenticated Linux SSH profile with Docker-internal gRPC, `query`, `explain`, plan-only `execute`, and `local_ydb_apply_schema action=validate` succeed without host port publication. Credential read, Docker target resolution, SSH listener setup, YDB readiness, session creation, session attach, and query execution failures return safe phase-specific diagnostics.
- Cleanup drops `managed_sql_smoke` even when an earlier check fails.
<!-- END MANAGED SQL SCENARIOS -->

## Scenario 0: Prerequisites

Goal: verify the target host has the required base tools before any Docker or YDB checks.

Profile:
`ghcr261-clean`

Calls:

```json
{ "tool": "local_ydb_check_prerequisites", "arguments": { "profile": "ghcr261-clean", "confirm": false } }
```

Optional install path on supported apt-based hosts:

```json
{ "tool": "local_ydb_check_prerequisites", "arguments": { "profile": "ghcr261-clean", "confirm": true } }
```

Expected:

- `ready=true` only when every prerequisite is usable
- the check reports Docker CLI availability separately from the `dockerDaemon` service check
- absent CLI/files appear in `missing`; a present CLI with an unreachable daemon appears in `unavailable`
- an unreachable SSH target reports `ready=false`, `missing=[]`, `unavailable=["target"]`, no installable packages, and no install plan; it does not infer that Docker, curl, ruby, or the password file is missing
- auth-enabled profiles also report whether `rootPasswordFile` exists
- plan-only output includes `apt-get` install commands only for supported auto-install packages
- after any confirmed `apt-get` attempt, `checks`, `ready`, `missing`, `unavailable`, package-manager fields, and manual actions describe a fresh post-install snapshot; `results` contains the install attempt followed by those final probes
- Docker installation and daemon startup remain manual; `confirm=true` never starts Docker

Avoid:

- treating `inventory = 0 containers` as proof that Docker is installed on a remote host
- proposing Docker or helper installation when the SSH target itself is unavailable
- using `confirm: true` blindly on a host where `apt-get` should not be touched

## Scenario 1: Preflight Read-Only Coverage

Goal: verify the selected profile is wired correctly and all read-only endpoints work.

Profile:
`ghcr261-clean`

Calls:

```json
{ "tool": "local_ydb_inventory", "arguments": { "profile": "ghcr261-clean" } }
{ "tool": "local_ydb_storage_leftovers", "arguments": { "profile": "ghcr261-clean" } }
{ "tool": "local_ydb_status_report", "arguments": { "profile": "ghcr261-clean" } }
{ "tool": "local_ydb_healthcheck", "arguments": { "profile": "ghcr261-clean" } }
{ "tool": "local_ydb_scheme", "arguments": { "profile": "ghcr261-clean" } }
{ "tool": "local_ydb_permissions", "arguments": { "profile": "ghcr261-clean" } }
```

Expected:

- successful `inventory` returns `ok=true`, `docker.cliAvailable=true`, `docker.daemonReachable=true`, and the current containers/volumes.
- Docker CLI, daemon, or inventory failures return `ok=false` with a reason and omit inventory arrays; never interpret that response as an empty host.
- `storage_leftovers` reports candidate volumes/paths without mutating them.
- `status_report` contains every component independently: inventory, auth, tenant, nodes, or health rejection produces the existing component-shaped safe fallback and does not prevent later checks.
- fallback diagnostics contain fixed summaries and empty command/output fields rather than raw exceptions, SSH/Docker stderr, credential paths, or `ENOENT` details.
- `healthcheck` returns the YDB `selfCheckResult`, issue counts, issue types, capped raw output, and truncated `issue_log` entries when present.
- a healthcheck called without `noCache` or `noMerge` returns empty requested/effective/unsupported arrays, `compatibilityFallback=false`, and `warnings=[]`; `status_report` uses this path and must not add compatibility probe commands.
- `scheme` and `permissions` default to the tenant root for read-only schema and ACL inspection.

Avoid:

- Accessing `inventory.containers` before checking `inventory.ok`.
- Treating `status_report.tenant=not-ok` as a transport failure. It often just means the stack is not bootstrapped yet.

## Scenario 1A: Schema Generate and Apply

Goal: verify structured YDB table DDL generation, SDK validation, confirm-gating, application, inspection, and cleanup.

Calls:

```json
{ "tool": "local_ydb_generate_schema", "arguments": { "profile": "ghcr261-auth", "validate": true, "statements": [{ "kind": "createTable", "tableName": "schema_apply_smoke", "columns": [{ "name": "id", "type": "Uint64", "notNull": true }, { "name": "value", "type": "Utf8" }], "primaryKey": ["id"], "indexes": [{ "name": "schema_apply_smoke_by_value", "columns": ["value"], "global": true }], "with": { "AUTO_PARTITIONING_BY_SIZE": { "token": "ENABLED" } } }] } }
{ "tool": "local_ydb_apply_schema", "arguments": { "profile": "ghcr261-auth", "action": "validate", "script": "CREATE TABLE `schema_apply_smoke` (\n  `id` Uint64 NOT NULL,\n  `value` Utf8,\n  INDEX `schema_apply_smoke_by_value` GLOBAL ON (`value`),\n  PRIMARY KEY (`id`)\n)\nWITH (\n  AUTO_PARTITIONING_BY_SIZE = ENABLED\n);" } }
{ "tool": "local_ydb_apply_schema", "arguments": { "profile": "ghcr261-auth", "action": "apply", "script": "CREATE TABLE `schema_apply_smoke` (\n  `id` Uint64 NOT NULL,\n  `value` Utf8,\n  INDEX `schema_apply_smoke_by_value` GLOBAL ON (`value`),\n  PRIMARY KEY (`id`)\n)\nWITH (\n  AUTO_PARTITIONING_BY_SIZE = ENABLED\n);", "confirm": false } }
{ "tool": "local_ydb_apply_schema", "arguments": { "profile": "ghcr261-auth", "action": "apply", "script": "CREATE TABLE `schema_apply_smoke` (\n  `id` Uint64 NOT NULL,\n  `value` Utf8,\n  INDEX `schema_apply_smoke_by_value` GLOBAL ON (`value`),\n  PRIMARY KEY (`id`)\n)\nWITH (\n  AUTO_PARTITIONING_BY_SIZE = ENABLED\n);", "confirm": true } }
{ "tool": "local_ydb_scheme", "arguments": { "profile": "ghcr261-auth", "action": "describe", "path": "/local/example/schema_apply_smoke" } }
{ "tool": "local_ydb_apply_schema", "arguments": { "profile": "ghcr261-auth", "action": "apply", "script": "DROP TABLE schema_apply_smoke;", "confirm": true } }
```

Expected:

- schema generation returns generated DDL, script SHA-256, statement kinds, official YDB references, risk, warnings, verification steps, and SDK validation when `validate=true`
- bare table `WITH` tokens such as `AUTO_PARTITIONING_BY_SIZE = ENABLED` are represented as `{ "token": "ENABLED" }` in the structured spec
- validation runs through the YDB JS SDK and does not apply DDL
- apply without `confirm=true` is plan-only after validation
- confirmed apply reports script SHA-256, statement kinds, validation/execution status, risk, rollback, and verification without echoing raw DDL or credential paths
- `DROP TABLE` and destructive `ALTER TABLE ... DROP ...` actions are high risk
- `CREATE TABLE` `notNull` is used only for columns that are part of `primaryKey`; non-key required business fields should be enforced by application validation or a later YDB feature path
- `partitionByHash` is used only with `store: "column"` and primary key columns; row tables use row partitioning `WITH` settings instead
- column names with the reserved `__ydb_` prefix, unsupported column-oriented table types, `ALTER TABLE ADD COLUMN` `notNull`/`default`, duplicate add/drop column actions, and generated scripts over 1 MiB are rejected before validation/application
- If an index needs a newly added column, generate/apply the `addColumn` first, then run a separate generate/apply call for `addIndex`; do not add an index on a column dropped in the same `alterTable` spec
- `vector_kmeans_tree` indexes include `global: true`, `sync: "sync"`, no `unique`, and complete `with` settings: `vector_dimension`, `vector_type`, either `distance` or `similarity`, `clusters`, and `levels`
- normal secondary indexes are global-only, do not accept creation-time `with` settings, unique indexes are synchronous, and creating a table with a vector index returns a warning that adding the vector index after loading representative data is preferred

Avoid:

- assuming generated DDL was applied; apply still goes through `local_ydb_apply_schema` and requires `confirm=true`
- using schema apply for DML, user/auth DDL, ACLs, topics, transfers, or views
- assuming rollback is automatic

## Scenario 1A.1: Diverse Schema Generate Probes

Goal: exercise the structured generator against common schema shapes before relying on it for a larger migration.

Calls:

```json
{ "tool": "local_ydb_generate_schema", "arguments": { "profile": "ghcr261-auth", "validate": true, "statements": [{ "kind": "createTable", "tableName": "schema_probe_column_partition", "store": "column", "partitionByHash": ["tenant_id"], "columns": [{ "name": "tenant_id", "type": "Utf8", "notNull": true }, { "name": "ts", "type": "Timestamp", "notNull": true }, { "name": "value", "type": "Double" }], "primaryKey": ["tenant_id", "ts"], "with": { "AUTO_PARTITIONING_MIN_PARTITIONS_COUNT": 2 } }] } }
{ "tool": "local_ydb_generate_schema", "arguments": { "profile": "ghcr261-auth", "validate": true, "statements": [{ "kind": "createTable", "tableName": "schema_probe_vector", "store": "row", "columns": [{ "name": "id", "type": "Uint64", "notNull": true }, { "name": "user", "type": "String" }, { "name": "title", "type": "String" }, { "name": "embedding", "type": "String" }], "primaryKey": ["id"], "indexes": [{ "name": "schema_probe_vector_idx", "columns": ["user", "embedding"], "cover": ["title"], "global": true, "sync": "sync", "using": "vector_kmeans_tree", "with": { "distance": "cosine", "vector_type": "float", "vector_dimension": 3, "clusters": 2, "levels": 1 } }] }] } }
{ "tool": "local_ydb_generate_schema", "arguments": { "profile": "ghcr261-auth", "validate": true, "statements": [{ "kind": "createTable", "tableName": "schema_probe_defaults", "columns": [{ "name": "id", "type": "Uint64", "notNull": true, "default": 1 }, { "name": "label", "type": "Utf8", "default": "new" }, { "name": "created_on", "type": "Date", "default": "2026-05-27" }], "primaryKey": ["id"] }] } }
{ "tool": "local_ydb_generate_schema", "arguments": { "profile": "ghcr261-auth", "validate": true, "statements": [{ "kind": "alterTable", "tableName": "schema_probe_alter", "actions": [{ "kind": "addColumn", "column": { "name": "status", "type": "Utf8" } }] }] } }
{ "tool": "local_ydb_generate_schema", "arguments": { "profile": "ghcr261-auth", "validate": true, "statements": [{ "kind": "alterTable", "tableName": "schema_probe_alter", "actions": [{ "kind": "addIndex", "index": { "name": "schema_probe_alter_by_status", "columns": ["status"], "global": true } }] }] } }
```

Expected:

- each positive generated script validates, then goes through `local_ydb_apply_schema action=apply confirm=false` before any confirmed apply
- created probe tables are described with `local_ydb_scheme action=describe` and then cleaned up with validated/confirmed `DROP TABLE`
- generator-only negative probes reject row-table `partitionByHash`, non-primary-key `partitionByHash`, empty `partitionByHash`/`cover`, column-store secondary indexes, unsupported column-store key/non-key types, local secondary indexes, secondary index `with` settings, async unique indexes, unique vector indexes, same-spec add/drop column references from indexes, duplicate add/drop column/index actions, `ALTER TABLE ADD COLUMN` `notNull`/`default`, `with.STORE`, reserved `__ydb_` column names, missing primary/index columns, invalid types, invalid setting names/tokens, and scripts over 1 MiB before rendering or validation

## Scenario 1B: Published Image Tags

Goal: verify that the registry tag listing tool can discover concrete `local-ydb` image versions before an upgrade.

Calls:

```json
{ "tool": "local_ydb_list_versions", "arguments": {} }
{ "tool": "local_ydb_list_versions", "arguments": { "image": "ghcr.io/ydb-platform/local-ydb", "pageSize": 50, "maxPages": 2 } }
```

Expected:

- the response includes `image`, `registry`, `repository`, `tags`, `count`, and `truncated`
- the default image resolves to `ghcr.io/ydb-platform/local-ydb`
- `tags` includes concrete patch tags when the registry publishes them
- numeric version tags are sorted newest first; mutable aliases such as `latest`, `nightly`, and `trunk` follow the numeric versions
- `truncated` becomes `true` only when the configured page limit is reached before the registry finishes pagination

Avoid:

- assuming `latest` is the only safe upgrade target
- using a short major/minor tag in production-like checks when an exact patch tag is available

## Scenario 1C: Background Image Pull

Goal: start slow registry downloads outside synchronous bootstrap or upgrade calls.

Calls:

```json
{ "tool": "local_ydb_pull_image", "arguments": { "profile": "ghcr261-clean", "image": "ghcr.io/ydb-platform/local-ydb:26.1.1.6", "confirm": false } }
{ "tool": "local_ydb_pull_image", "arguments": { "profile": "ghcr261-clean", "image": "ghcr.io/ydb-platform/local-ydb:26.1.1.6", "confirm": true } }
{ "tool": "local_ydb_pull_status", "arguments": { "jobId": "<jobId-from-pull-image>" } }
```

Expected:

- plan-only output includes `docker image inspect` and `docker pull`
- with `confirm: true`, the tool returns quickly with `status: running` and a `jobId`, unless the image is already present
- status polling returns a monotonic integer `progressPercent` based on completed known Docker layers, starting at `0` and remaining below `100` while the pull is running
- successful completion returns `status: completed` with `progressPercent: 100`; failure returns `status: failed` with the last observed percentage
- bootstrap and upgrade image preflight failures point back to `local_ydb_pull_image` instead of hanging inside `docker run`

Avoid:

- relying on `docker run` to implicitly pull large images inside a synchronous MCP tool call
- interpreting `progressPercent` as exact byte-level progress
- treating a 120-second MCP client timeout during image download as a YDB bootstrap failure

## Scenario 2: Fresh Root Database Bootstrap

Goal: validate network/volume/static-node bring-up for plain `/local` without creating a CMS tenant or dynamic node.

Profile:
`ghcr261-clean`

Calls:

```json
{ "tool": "local_ydb_bootstrap_root_database", "arguments": { "profile": "ghcr261-clean", "confirm": false } }
{ "tool": "local_ydb_bootstrap_root_database", "arguments": { "profile": "ghcr261-clean", "confirm": true } }
{ "tool": "local_ydb_scheme", "arguments": { "profile": "ghcr261-clean", "path": "/local" } }
```

Expected:

- plan-only output starts the static container only
- no `admin database /local/... create` command is planned
- no dynamic-node container is created
- `scheme ls /local` succeeds through the static gRPC endpoint

Avoid:

- using the tenant bootstrap tool when the task only needs `/local`
- treating a missing configured tenant as a root database failure

## Scenario 2A: Restart a Compatible Stopped Static Container

Goal: verify bootstrap reuses a task-owned stopped static container only when its stored configuration remains compatible.

Precondition:
bootstrap a disposable profile, then stop only that profile's static container.

Calls:

```json
{ "tool": "local_ydb_bootstrap_root_database", "arguments": { "profile": "<disposable-profile>", "confirm": true } }
{ "tool": "local_ydb_healthcheck", "arguments": { "profile": "<disposable-profile>", "databasePath": "/local" } }
```

Expected:

- bootstrap applies the same compatibility checks to running and stopped containers and never relies on `docker port`
- the exact image reference and current image ID, selected network, `/ydb_data` volume or bind source/type/RW, complete loopback gRPC and monitoring bindings without extras, required environment, `unless-stopped` policy, and disabled healthcheck must all match
- tenant bootstrap and restart additionally require the GraphShard feature flag plus the static gRPC binding and every configured dynamic gRPC binding
- a static container created for a smaller `dynamicNodeCount` fails both bootstrap and restart compatibility before any configured dynamic container is mutated and requires destroy/rebootstrap
- an inspect failure or mismatch returns only the incompatible aspect plus recreation guidance and leaves the container stopped; changing the profile volume is a useful live negative control
- a compatible static container starts exactly once and the root healthcheck succeeds

Avoid:

- stopping or reusing a persisted `/local` stack owned by another workflow
- starting, removing, or automatically recreating a container whose stored configuration does not match the selected operation

## Scenario 3: Fresh Bootstrap on an Isolated GHCR Stack

Goal: validate network/volume/static/dynamic bring-up on a clean profile.

Profile:
`ghcr261-clean`

Calls:

```json
{ "tool": "local_ydb_bootstrap", "arguments": { "profile": "ghcr261-clean", "confirm": false } }
{ "tool": "local_ydb_bootstrap", "arguments": { "profile": "ghcr261-clean", "confirm": true } }
```

Expected:

- Docker network and volume are created.
- Static container starts.
- `admin database /local/example status` succeeds; `PENDING_RESOURCES` is acceptable before the first dynamic node fully serves traffic.
- Dynamic container is recreated with the current launch command if needed.
- Final checks succeed:
  `scheme ls /local/example`, viewer capabilities, dynamic node registration.

What made this work:

- exact image tag `ghcr.io/ydb-platform/local-ydb:26.1.1.6`
- dynamic launch sanitizes `grpc_config.ca/cert/key` from the generated config before calling `/ydbd server`
- dynamic launch disables TLS with:
  `GRPC_TLS_PORT=`
  `YDB_GRPC_ENABLE_TLS=0`

Avoid:

- using `ghcr.io/ydb-platform/local-ydb:26.1`
- reusing a stale dynamic container with `docker start` if its original launch command was broken

## Scenario 4: Explicit Tenant and Dynamic-Node Smoke Test

Goal: exercise tenant creation and dynamic start as separate tools.

Profile:
`ghcr261-clean`

Calls:

```json
{ "tool": "local_ydb_create_tenant", "arguments": { "profile": "ghcr261-clean", "confirm": false } }
{ "tool": "local_ydb_create_tenant", "arguments": { "profile": "ghcr261-clean", "confirm": true } }
{ "tool": "local_ydb_database_status", "arguments": { "profile": "ghcr261-clean" } }
{ "tool": "local_ydb_start_dynamic_node", "arguments": { "profile": "ghcr261-clean", "confirm": false } }
{ "tool": "local_ydb_start_dynamic_node", "arguments": { "profile": "ghcr261-clean", "confirm": true } }
{ "tool": "local_ydb_tenant_check", "arguments": { "profile": "ghcr261-clean" } }
```

Expected:

- `create_tenant` waits until `admin database ... status` is readable. It should not insist on `RUNNING` before the first dynamic node.
- `database_status` can show `PENDING_RESOURCES` before dynamic registration and `RUNNING` afterwards.
- `start_dynamic_node` recreates the container if it is stale or exited, but first verifies that the static container still matches the current image ID and full configured topology; the recreated container starts only after its resolved image ID matches the static node.
- `tenant_check` succeeds only after the dynamic node is actually serving the tenant gRPC path.

Avoid:

- assuming `create OK` alone means the tenant is resolvable by NodeBroker

## Scenario 5: Runtime Diagnostics

Goal: cover the focused read-only diagnostics used when bootstrap fails.

Profile:
`ghcr261-clean`

Calls:

```json
{ "tool": "local_ydb_database_status", "arguments": { "profile": "ghcr261-clean" } }
{ "tool": "local_ydb_healthcheck", "arguments": { "profile": "ghcr261-clean", "noCache": true, "noMerge": true } }
{ "tool": "local_ydb_container_logs", "arguments": { "profile": "ghcr261-clean", "target": "static", "lines": 120 } }
{ "tool": "local_ydb_container_logs", "arguments": { "profile": "ghcr261-clean", "target": "dynamic", "lines": 120 } }
{ "tool": "local_ydb_nodes_check", "arguments": { "profile": "ghcr261-clean" } }
{ "tool": "local_ydb_graphshard_check", "arguments": { "profile": "ghcr261-clean" } }
{ "tool": "local_ydb_storage_placement", "arguments": { "profile": "ghcr261-clean" } }
```

Expected:

- `healthcheck` gives the official YDB self-check status and issue hierarchy before falling back to narrower local heuristics.
- `noCache` and `noMerge` request desired semantics. A modern CLI keeps both in `optionResolution.effective`, returns `unsupported=[]`, `compatibilityFallback=false`, and `warnings=[]` in one command.
- an older CLI may reject a requested option with the exact `NLastGetopt::TUsageException`/`healthcheck --help` signature. The tool removes one rejected flag per immediate retry, uses at most three total calls for both options, and returns the final health result with the dropped names in `optionResolution.unsupported`, `compatibilityFallback=true`, warnings, and the summary suffix `Compatibility fallback applied; inspect warnings.`
- an exact rejection is recorded before the retry deadline check. If the shared deadline expires before a retry can start, the tool makes one call, reports the rejected option as unsupported with its warning, keeps `compatibilityFallback=false`, and does not add the compatibility summary suffix.
- if `noCache` is unsupported, cache bypass was not guaranteed; if `noMerge` is unsupported, issue entries may have been merged. Do not describe the result as fresh or unmerged unless the corresponding option remains in `optionResolution.effective`.
- only final-attempt command/stdout/stderr and byte metadata are returned. Timeout, auth, transport, invalid JSON, `DEGRADED`, unrelated parser failures, unexpected stderr lines, and errors for flags that were not requested are never compatibility retries.
- `container_logs(dynamic)` shows whether the node:
  registered,
  fetched config,
  crashed on TLS/cert,
  or failed tenant resolution.
- `container_logs(static)` shows `NodeBroker` and `SchemeShard` evidence for create/resolve problems.
- `nodes_check` and `graphshard_check` become useful after the stack is healthy or after auth is enabled with a valid viewer session path.
- `storage_placement` proves the tenant’s groups are on `/ydb_data/pdisks/1`.

Avoid:

- using generic `docker logs` or shell-only inspection before trying `local_ydb_container_logs`

## Scenario 6: Idempotent Restart

Goal: confirm the restart tool is safe and uses the current launch command.

Profile:
`ghcr261-clean`

Calls:

```json
{ "tool": "local_ydb_restart_stack", "arguments": { "profile": "ghcr261-clean", "confirm": false } }
{ "tool": "local_ydb_restart_stack", "arguments": { "profile": "ghcr261-clean", "confirm": true } }
{ "tool": "local_ydb_status_report", "arguments": { "profile": "ghcr261-clean" } }
```

Expected:

- inventory and the full check-only static compatibility preflight run before any container stop, remove, or start command
- a static binding mismatch fails without changing configured or one-off container IDs/states and requires destroy/bootstrap
- after a successful preflight, the static node restarts first
- tenant status is checked before dynamic node is started again
- every configured dynamic node is unconditionally recreated, including a container observed in Docker's restarting state
- rollback uses `local_ydb_restart_stack` or `local_ydb_bootstrap`, not an inventory claim about removed configured definitions
- post-restart `status_report` returns `tenant=ok`, `nodes=ok`

Avoid:

- trusting a plain `docker start <dynamic>` path for a container created with old flags

## Scenario 7: Dump and Restore

Goal: prove backup/restore on a clean GHCR stack.

Profiles:

- source: `local`
- target: `ghcr261-clean`

Calls:

```json
{ "tool": "local_ydb_dump_tenant", "arguments": { "profile": "local", "confirm": true, "dumpName": "pre-auth-mcp-20260425" } }
{ "tool": "local_ydb_list_dumps", "arguments": { "profile": "ghcr261-clean" } }
{ "tool": "local_ydb_restore_tenant", "arguments": { "profile": "ghcr261-clean", "confirm": true, "dumpName": "pre-auth-mcp-20260425" } }
{ "tool": "local_ydb_tenant_check", "arguments": { "profile": "ghcr261-clean" } }
{ "tool": "local_ydb_graphshard_check", "arguments": { "profile": "ghcr261-clean" } }
```

Path-level example:

```json
{ "tool": "local_ydb_dump_tenant", "arguments": { "profile": "local", "confirm": true, "dumpName": "one-table-smoke", "path": "dir/table" } }
{ "tool": "local_ydb_restore_tenant", "arguments": { "profile": "ghcr261-clean", "confirm": true, "dumpName": "one-table-smoke", "path": ".", "describePaths": ["dir/table"], "countQueries": [{ "label": "dir/table rows", "query": "SELECT COUNT(*) FROM `dir/table`;" }] } }
```

For dump, `path` is the source object or directory for `ydb tools dump -p`. For restore, `path` is the destination directory for `ydb tools restore -p`; restoring a single table dump back under the tenant root normally uses `path: "."`.

Expected:

- dump helper container runs with `--entrypoint /bin/bash`
- list-dumps reports dump directories that contain a `tenant` folder
- restore helper container runs with `--entrypoint /bin/bash`
- restored tenant returns `.metadata  .sys`
- GraphShard exists after restore

Avoid:

- assuming the helper image entrypoint can run arbitrary shell commands without `--entrypoint /bin/bash`

## Scenario 8: Auth Artifact Preparation

Goal: test the two new preparation tools before mutating the running stack.

Profile:
`ghcr261-auth`

Calls:

```json
{ "tool": "local_ydb_prepare_auth_config", "arguments": { "profile": "ghcr261-auth", "confirm": false } }
{ "tool": "local_ydb_prepare_auth_config", "arguments": { "profile": "ghcr261-auth", "confirm": true } }
{ "tool": "local_ydb_write_dynamic_auth_config", "arguments": { "profile": "ghcr261-auth", "confirm": false } }
{ "tool": "local_ydb_write_dynamic_auth_config", "arguments": { "profile": "ghcr261-auth", "confirm": true } }
```

Expected:

- `prepare_auth_config` writes:
  `/tmp/local-ydb-auth/config.auth.yaml`
  `/tmp/local-ydb-auth/root.password`
- generated auth config includes:
  `enforce_user_token_requirement: true`
  `viewer_allowed_sids`
  `monitoring_allowed_sids`
  `administration_allowed_sids`
  `register_dynamic_node_allowed_sids`
- viewer/admin allowed SIDs include both `root` and `root@builtin`
- `write_dynamic_auth_config` writes:
  `StaffApiUserToken: "root@builtin"`
  `NodeRegistrationToken: "root@builtin"`

Avoid:

- assuming the viewer/admin SID is only `root@builtin`
- assuming the default root token identifies as `root@builtin`; in our run `whoami` reported `User SID: root`

## Scenario 9: Auth Rollout

Goal: turn a healthy clean stack into an auth-enabled stack while keeping clients stopped and public monitoring inaccessible. Run Scenario 10A next, then Scenario 10 before admitting clients.

Profile:
`ghcr261-auth`

Calls:

```json
{ "tool": "local_ydb_apply_auth_hardening", "arguments": { "profile": "ghcr261-auth", "confirm": false } }
{ "tool": "local_ydb_apply_auth_hardening", "arguments": { "profile": "ghcr261-auth", "confirm": true } }
```

Expected:

- the full check-only static compatibility preflight runs before config copy or any container mutation; a mismatch leaves IDs/states unchanged and requires destroy/bootstrap
- the reviewed config is copied into the static container
- dynamic node is stopped
- static node is restarted
- tenant status remains readable via password
- dynamic node is recreated with:
  `--auth-token-file /run/local-ydb/dynamic-node-auth.pb`
  sanitized dynamic config
  TLS disabled for local mode
- rollback restores the static config and uses `local_ydb_restart_stack` or `local_ydb_bootstrap` to recreate configured nodes, never `docker start` for removed definitions

Avoid:

- restarting a stale dynamic auth container without recreation
- using a hardcoded login URL on `8765` when the profile runs on another monitoring port

## Scenario 10A: Root Password Rotation

Goal: replace the known default root password before shared or exposed use, without exposing it in plan output.

Profile:
`ghcr261-auth`

Prerequisites:

- Scenario 9 has enabled auth; clients remain stopped and public monitoring remains inaccessible.
- The selected profile has prepared `authConfigPath` and `rootPasswordFile`.
- Choose a unique non-default password accepted by the configured password policy; the example uses only a placeholder.
- Retain the old credential only in a protected password file for the negative login check; never print it or put it in process arguments.

Calls:

```json
{ "tool": "local_ydb_set_root_password", "arguments": { "profile": "ghcr261-auth", "password": "<new-password>", "confirm": false } }
{ "tool": "local_ydb_set_root_password", "arguments": { "profile": "ghcr261-auth", "password": "<new-password>", "confirm": true } }
```

Review the plan before issuing the confirmed call. A plan-only response does not rotate credentials.

Expected:

- plan-only output does not print the raw password
- the confirmed tool rotates the runtime password with `ALTER USER`, synchronizes the host auth config and `root.password`, and checks authenticated tenant access and anonymous denial
- every execution stage must succeed; `executed: true` alone only records that execution was attempted

Check the confirmed response as `rotation`:

```js
const rotationSucceeded =
  rotation.executed === true &&
  rotation.results?.length === 4 &&
  rotation.results.every(({ ok }) => ok === true);
```

- The host auth config and password file must match the new password; verify without printing either credential.
- The new password must authenticate successfully through a fresh login.
- The old password must be rejected by a fresh login because of invalid credentials. Use separate sessions without existing cookies or tokens; transport, timeout and endpoint failures do not establish rejection.
- Check the lockout policy before making at most one negative login attempt. Do not loop on rejected credentials; password-login rejection is not a claim that existing tokens were revoked.
- Anonymous `viewer/json/whoami` must still return `401`; run Scenario 10 using the new root password before admitting clients.
- The tool leaves `${authConfigPath}.before-local-ydb-toolkit-password-rotate` and `${rootPasswordFile}.before-local-ydb-toolkit-password-rotate`. After post-auth verification, close the explicit rollback hold and retire these obsolete credential backups and the old-password verification file under the Obsolete Credential Backups policy in `auth-hardening.md`.
- Empty passwords are an upstream YDB capability, but this MCP tool requires a non-empty `password` argument.
- If `auth_config.password_complexity` is configured, the new value must satisfy it.

Failure handling:

Keep the stack isolated if any execution stage fails or the outcome is unknown. The runtime password may have changed even if host credential/config synchronization failed. Establish which credential currently authenticates and whether the host artifacts match before recovery. Do not retry blindly or automatically restore the weak default password.

Avoid:

- storing the password directly in committed config
- changing the password on a profile that lacks `authConfigPath` or `rootPasswordFile`
- assuming every punctuation mark is portable across builds; prefer letters, digits, and documented YDB special characters `!@#$%^&*()_+{}|<>?=` unless the target image has already been rehearsed with a broader set

## Scenario 10: Post-Auth Verification

Goal: prove the auth rollout and mandatory password rotation worked before admitting clients or exposing monitoring.

Prerequisite: Scenario 10A must pass, including all execution stages, synchronized host artifacts, fresh new-password success and old-password rejection.

Profile:
`ghcr261-auth`

Calls:

```json
{ "tool": "local_ydb_auth_check", "arguments": { "profile": "ghcr261-auth" } }
{ "tool": "local_ydb_status_report", "arguments": { "profile": "ghcr261-auth" } }
{ "tool": "local_ydb_nodes_check", "arguments": { "profile": "ghcr261-auth" } }
{ "tool": "local_ydb_graphshard_check", "arguments": { "profile": "ghcr261-auth" } }
{ "tool": "local_ydb_database_status", "arguments": { "profile": "ghcr261-auth" } }
```

Expected:

- client admission remains blocked until the explicit rollback hold is closed and obsolete credential backups have been retired and verified under the `auth-hardening.md` policy
- `auth_check.viewerWhoamiStatus == 401`
- authenticated tenant metadata works with the new root password
- `status_report` returns `tenant=ok`, `nodes=ok`
- `nodes_check` returns the dynamic node
- `graphshard_check` reports `GraphShardExists=true`
- `database_status` returns `State: RUNNING`

Avoid:

- treating a `401` on `/viewer/json/whoami` as an error after auth; it is the expected anonymous result

## Scenario 11: Add Extra Dynamic Nodes

Goal: add multiple dynamic nodes to a healthy auth-enabled stack without creating extra profile entries.

Profile:
`ghcr261-auth`

Calls:

```json
{ "tool": "local_ydb_add_dynamic_nodes", "arguments": { "profile": "ghcr261-auth", "count": 2, "confirm": false } }
{ "tool": "local_ydb_add_dynamic_nodes", "arguments": { "profile": "ghcr261-auth", "count": 2, "confirm": true } }
{ "tool": "local_ydb_add_dynamic_nodes", "arguments": { "profile": "ghcr261-auth", "startIndex": 2, "confirm": false } }
{ "tool": "local_ydb_nodes_check", "arguments": { "profile": "ghcr261-auth" } }
{ "tool": "local_ydb_tenant_check", "arguments": { "profile": "ghcr261-auth" } }
{ "tool": "local_ydb_container_logs", "arguments": { "profile": "ghcr261-auth", "target": "dynamic", "lines": 80 } }
```

Expected:

- plan-only output creates one-off containers `ydb-dyn-example-ghcr261-4` and `ydb-dyn-example-ghcr261-5`
- default ports are derived from the profile:
  `2260/9069/19305` and `2261/9070/19306`
- dynamic containers mount `/tmp/local-ydb-auth/dynamic-node-auth.pb` when auth is enabled
- `confirm=true` starts one node, verifies its exact container is stably running and its IC port appears in `nodelist`, then starts the next
- explicit `startIndex: 2` is rejected before a mutating plan because configured indexes `1..3` cannot be used for one-off add; configured container IDs remain unchanged
- `nodes_check` reports five dynamic nodes total: three configured nodes plus the two one-off nodes
- tenant metadata remains reachable

Avoid:

- using any `startIndex <= 3`; configured indexes belong to the declarative topology
- adding many nodes at once on a live auth stack without first checking logs and `nodelist`

Rollback:

```bash
docker rm -f ydb-dyn-example-ghcr261-4 ydb-dyn-example-ghcr261-5
```

## Scenario 12: Remove Extra Dynamic Nodes

Goal: keep default removal inside one-off capacity while allowing deliberate configured-node drift fixtures.

Profile:
`ghcr261-auth`

Calls:

```json
{ "tool": "local_ydb_remove_dynamic_nodes", "arguments": { "profile": "ghcr261-auth", "confirm": false } }
{ "tool": "local_ydb_remove_dynamic_nodes", "arguments": { "profile": "ghcr261-auth", "confirm": true } }
{ "tool": "local_ydb_nodes_check", "arguments": { "profile": "ghcr261-auth" } }
```

Expected:

- immediately after Scenario 11, default plan-only output targets the highest one-off suffix, `ydb-dyn-example-ghcr261-5`
- `confirm=true` removes that container and verifies its IC port disappears from authenticated `nodelist`
- rollback for the removed one-off node uses `local_ydb_add_dynamic_nodes` with matching suffixes and ports, not restart/bootstrap
- configured containers `ydb-dyn-example-ghcr261`, `-2`, and `-3` remain running with unchanged Docker IDs
- after all one-off nodes are removed, another default call fails with `found 0` and returns no destructive plan
- tenant metadata remains reachable after removal

Explicit configured-node drift fixture:

```json
{ "tool": "local_ydb_remove_dynamic_nodes", "arguments": { "profile": "ghcr261-auth", "confirm": false, "containers": ["ydb-dyn-example-ghcr261-2"] } }
{ "tool": "local_ydb_remove_dynamic_nodes", "arguments": { "profile": "ghcr261-auth", "confirm": false, "nodeIds": [50001] } }
```

Configured suffix `-2` is removable only through an explicit container, node ID, or `startIndex: 2` selector. Its removal creates runtime drift; rollback uses `local_ydb_restart_stack` or `local_ydb_bootstrap`, never `local_ydb_add_dynamic_nodes`. Mixed configured and one-off selections return both rollback instructions in that order.

Avoid:

- treating the profile's main `dynamicContainer` as removable through this tool
- assuming default removal can select configured suffixes
- using `nodeIds` for the base dynamic node; only IDs that resolve to suffix containers are removable
- removing multiple extra nodes at once on a live stack without checking `nodelist` after each removal

## Scenario 13: Add Storage Groups

Goal: increase `NumGroups` for a tenant storage pool by rereading and redefining the current pool shape.

Profile:
`ghcr261-auth`

Calls:

```json
{ "tool": "local_ydb_add_storage_groups", "arguments": { "profile": "ghcr261-auth", "count": 1, "confirm": false } }
{ "tool": "local_ydb_add_storage_groups", "arguments": { "profile": "ghcr261-auth", "count": 1, "confirm": true } }
{ "tool": "local_ydb_storage_placement", "arguments": { "profile": "ghcr261-auth" } }
{ "tool": "local_ydb_tenant_check", "arguments": { "profile": "ghcr261-auth" } }
```

Expected:

- plan-only output targets tenant pool `/local/example:hdd`
- the generated `DefineStoragePool` request preserves the current pool fields and increases only `NumGroups`
- `confirm=true` succeeds without breaking tenant metadata
- post-change `ReadStoragePool` reports a higher `NumGroups` for the tenant pool
- `QueryBaseConfig` reflects the updated group set on the current PDisk layout

Avoid:

- treating `DecommitGroups` or `storage_units_to_remove` as a pool expansion path
- using a partial `DefineStoragePool` shape that drops `PDiskFilter`, `ScopeId`, or `ItemConfigGeneration`

## Scenario 14: Destroy Stack

Goal: remove tenant metadata, local-ydb nodes, Docker network, and profile storage from one tool.

Recommended disposable profile:
`ghcr-rebuild-clean`

Calls:

```json
{ "tool": "local_ydb_destroy_stack", "arguments": { "profile": "ghcr-rebuild-clean", "confirm": false } }
```

Optional shared-host-path cleanup:

```json
{ "tool": "local_ydb_destroy_stack", "arguments": { "profile": "ghcr-rebuild-clean", "confirm": false, "removeDumpHostPath": true, "removeAuthArtifacts": true } }
```

Expected:

- plan-only output removes tenant metadata first when the static node is reachable
- extra dynamic nodes are removed before the profile's main dynamic container
- the static container, Docker network, and Docker volume are removed
- bind-mounted data is not deleted unless `removeBindMountPath: true`
- auth files and dump directories are not deleted unless explicitly requested

Avoid:

- enabling host-path deletion flags on shared paths without checking whether other profiles use them
- using this tool with `confirm=true` on a profile you still need without first taking a dump

## Scenario 15: Reduce Storage Groups By Rebuild

Goal: reduce a tenant pool from a larger `NumGroups` back to a smaller one without relying on an unverified live shrink path.

Profile:
`ghcr261-auth`

Calls:

```json
{ "tool": "local_ydb_reduce_storage_groups", "arguments": { "profile": "ghcr261-auth", "count": 1, "dumpName": "shrink-smoke", "confirm": false } }
```

Expected:

- plan-only output starts with a tenant dump
- the stack is rebuilt with `admin database /local/example create hdd:1`
- auth-enabled profiles re-run:
  `local_ydb_prepare_auth_config`
  `local_ydb_write_dynamic_auth_config`
  `local_ydb_apply_auth_hardening`
- extra dynamic-node suffixes are re-added after restore/auth reapply
- every one-off node keeps its inspected gRPC, monitoring, and IC ports; an incomplete inspect aborts before dump or destroy

Avoid:

- treating `DefineStoragePool { NumGroups: smaller }` as a proven live shrink path
- deleting auth artifacts during the rebuild path for an auth-enabled profile

## Scenario 15A: Version Upgrade By Rebuild

Goal: upgrade a working profile to a specific image tag without reusing the old volume in place.

Profile:
`ghcr261-auth`

Calls:

```json
{ "tool": "local_ydb_upgrade_version", "arguments": { "profile": "ghcr261-auth", "version": "26.1.1.6", "confirm": false } }
```

Optional execution path on a disposable stack:

```json
{ "tool": "local_ydb_upgrade_version", "arguments": { "profile": "ghcr261-auth", "version": "<target-tag>", "dumpName": "upgrade-smoke", "confirm": true } }
```

Expected:

- the plan starts with source and target image preflight checks
- if either image is missing, run `local_ydb_pull_image` first and retry after `local_ydb_pull_status` reports completion
- after image preflight, the upgrade path performs dump, destroy, bootstrap, restore, auth reapply, and extra dynamic-node recreation in that order
- before dump or destroy, every one-off node's exact gRPC, monitoring, and IC ports are inspected and retained; an incomplete definition aborts the rebuild
- auth-enabled profiles re-run:
  `local_ydb_prepare_auth_config`
  `local_ydb_write_dynamic_auth_config`
  `local_ydb_apply_auth_hardening`
- successful final inventory verifies the recreated containers' image tags and then persists `profiles.<name>.image` in the file-backed config
- a verified image mismatch returns the accumulated history and leaves the profile image unchanged
- if final inventory is unavailable only after dump/rebuild/restore/auth/node phases succeed, the response appends a safe failed verification result, omits `imageVerification`, preserves the full history, and persists the target profile image for subsequent operations

Avoid:

- using this tool against a profile pinned by image digest
- using this tool against a profile with `bindMountPath`; automatic version upgrade only supports volume-backed rebuilds
- treating it as an in-place rolling upgrade of the existing volume
- skipping the explicit target tag check from `local_ydb_list_versions`

## Scenario 16: Cleanup Candidates

Goal: test the dangerous cleanup tool only on disposable targets.

Recommended disposable targets:

- stale rehearsal volumes discovered by `storage_leftovers`
- old test dump directories under `/tmp/local-ydb-dump/...`
- explicitly unused side-by-side rehearsal volumes such as `ydb-local-data-ghcr-clean` only after you have decided they are no longer needed

Calls:

```json
{ "tool": "local_ydb_storage_leftovers", "arguments": { "profile": "ghcr261-auth" } }
{ "tool": "local_ydb_cleanup_storage", "arguments": { "profile": "ghcr261-auth", "confirm": false, "volumes": ["<known-disposable-volume>"] } }
{ "tool": "local_ydb_cleanup_storage", "arguments": { "profile": "ghcr261-auth", "confirm": false, "paths": ["/tmp/local-ydb-dump/<known-disposable-dump>"] } }
```

Expected:

- plan-only output includes the exact `docker volume rm` or `rm -rf` target
- unsafe targets like `/tmp`, `/var/lib/docker`, or unrelated names are rejected by validation

Avoid:

- using `cleanup_storage(confirm=true)` against any active profile volume or the current auth stack

## Coverage Matrix

- Bootstrap and lifecycle:
  `local_ydb_bootstrap_root_database`, `local_ydb_bootstrap`, `local_ydb_create_tenant`, `local_ydb_start_dynamic_node`, `local_ydb_add_dynamic_nodes`, `local_ydb_remove_dynamic_nodes`, `local_ydb_restart_stack`
- Version discovery:
  `local_ydb_list_versions`
- Image pulls:
  `local_ydb_pull_image`, `local_ydb_pull_status`
- Storage-pool expansion:
  `local_ydb_add_storage_groups`
- Storage-pool reduction by rebuild:
  `local_ydb_reduce_storage_groups`
- Version upgrade by rebuild:
  `local_ydb_upgrade_version`
- Full teardown:
  `local_ydb_destroy_stack`
- Backup and restore:
  `local_ydb_list_dumps`, `local_ydb_dump_tenant`, `local_ydb_restore_tenant`
- Auth rollout:
  `local_ydb_prepare_auth_config`, `local_ydb_write_dynamic_auth_config`, `local_ydb_apply_auth_hardening`, `local_ydb_set_root_password`, `local_ydb_permissions`, `local_ydb_auth_check`
- Managed SQL:
  `local_ydb_sql`
- Read-only diagnostics:
  `local_ydb_inventory`, `local_ydb_database_status`, `local_ydb_healthcheck`, `local_ydb_container_logs`, `local_ydb_status_report`, `local_ydb_tenant_check`, `local_ydb_scheme`, `local_ydb_permissions`, `local_ydb_nodes_check`, `local_ydb_graphshard_check`, `local_ydb_storage_placement`, `local_ydb_storage_leftovers`
- Cleanup:
  `local_ydb_cleanup_storage`

## Known Working Baseline

Field-proven successful stack in this repo:

- image: `ghcr.io/ydb-platform/local-ydb:26.1.1.6`
- clean profile: `ghcr261-clean`
- auth profile: `ghcr261-auth`
- dump name used successfully: `pre-auth-mcp-20260425`
- auth files:
  `/tmp/local-ydb-auth/config.auth.yaml`
  `/tmp/local-ydb-auth/root.password`
  `/tmp/local-ydb-auth/dynamic-node-auth.pb`

Successful end state:

- anonymous `viewer/json/whoami` returns `401`
- authenticated `scheme ls /local/example` succeeds
- authenticated `nodelist` returns the dynamic node
- authenticated `capabilities` reports `GraphShardExists=true`
