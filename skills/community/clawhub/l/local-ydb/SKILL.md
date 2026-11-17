---
name: local-ydb
description: Operate local-ydb deployments, especially Docker setups using ghcr.io/ydb-platform/local-ydb, CMS-created tenants, GraphShard metrics, dynamic nodes, managed YQL query/explain/execute, structured table DDL generation/validation/application, YDB static credentials, auth hardening, monitoring exposure, storage pool changes, single-disk rebuilds, rollback planning, upstream ydb-platform/ydb source lookup through gh api, and troubleshooting local-ydb readiness, TLS, anonymous access, or viewer/json graph endpoints.
---

# Local YDB

## Purpose

Use this skill to inspect, document, run, harden, troubleshoot, or generate and apply table schemas for `local-ydb` deployments. Keep reusable operational recipes separate from one-off cutover notes, host paths, timestamps, and secrets.

## Execution Boundary

- Operate a deployment only when the active agent has a local shell or the `local_ydb_*` MCP tools connected to the target machine. A chat-only or remote environment cannot inspect the user's Docker daemon, files, or YDB endpoints.
- When local execution is unavailable, provide a bounded plan, configuration guidance, or commands for the user to run. State that the target was not inspected and do not report inferred health, inventory, or mutation results as observed facts.
- Plugin MCP processes start from the installed plugin root. Pass an absolute `configPath` to profile-based tools or configure `LOCAL_YDB_TOOLKIT_CONFIG` in the MCP client; do not assume a project-local `local-ydb.config.json` is the process working-directory default.
- Keep every mutation plan-first regardless of execution surface. Require the existing confirmation boundary before applying changes and preserve rollback and verification steps.

## First Steps

1. Identify the task type: documentation cleanup, local bootstrap, live inspection, managed YQL query/explain/execute, schema generation/apply, auth hardening, storage expansion, monitoring exposure, TLS investigation, or troubleshooting.
2. Determine whether the target is repo documentation, a local Docker stack, or a live remote host. Treat live Docker/YDB changes as medium to high risk; collect read-only state first and ask before destructive or externally visible mutations.
3. Check nearby project docs before editing reusable runbooks. Prefer existing setup, runbook, and auth notes over inventing a new topology.
4. Keep secrets and private host details out of public docs and skill output. Use placeholders for password files, private keys, IPs, domains, users, and backup paths unless the user explicitly asks for private operational notes.

## Reference Selection

- Read `references/topology.md` when starting or documenting static nodes, dynamic nodes, tenants, GraphShard, storage pools, or upstream YDB source lookups.
- Read `references/auth-hardening.md` when working on mandatory auth, static username/password credentials, monitoring access, reverse-proxy exposure, or TLS.
- Read `references/storage-migration.md` when adding PDisks, changing storage placement, moving storage onto one physical disk, creating replacement tenants, migrating data, decommissioning groups, reclaiming space, cleaning old Docker volumes/PDisks/dumps, or debugging why UI and BSC disagree about storage.
- Read `references/verification.md` when checking health, tenant state, GraphShard, graph data, storage, or auth behavior.
- Read `references/mcp-tool-scenarios.md` when testing MCP tools, exercising the managed SQL safety matrix, planning structured schema generation/apply flows, or building reusable generate-then-validate-then-apply examples.
- Read `references/history-and-non-goals.md` when cleaning docs, deciding what is reusable versus artifact noise, or reconciling stale hardening plans with final topology.
- For exact-GHCR `26.1.1.6` local runs, combine `topology.md`, `auth-hardening.md`, and `verification.md`; they contain field-proven steps for fresh bootstrap, restore, auth rollout, and the nightly-vs-stable pitfalls we hit in practice.
- Prefer the MCP read-only tools `local_ydb_inventory`, `local_ydb_status_report`, `local_ydb_healthcheck`, `local_ydb_database_status`, `local_ydb_container_logs`, and `local_ydb_storage_placement` over ad hoc shell diagnostics when they are available.

## Core Rules

- Do not assume `/local` has GraphShard. `YDB_FEATURE_FLAGS=enable_graph_shard` is necessary but not sufficient; use a CMS-created tenant such as `/local/<tenant>`.
- For a plain root `/local` database, use the root-only MCP bootstrap path instead of the tenant/dynamic-node bootstrap.
- Treat `profile.dynamicNodeCount` as the total declarative tenant-node count, including the primary node. Configured dynamic names must be distinct from the static container, and standalone primary start uses the same shared-network port validation as bootstrap. Tenant bootstrap publishes static gRPC and every configured dynamic gRPC port on loopback through the static container; one-off nodes do not change those bindings. Before any restart or auth-hardening mutation, require the existing static container to match the full profile and exact configured bindings; a mismatch requires destroy/bootstrap and must leave configured and one-off containers untouched. Bootstrap and compatible restart reconcile nodes `1..N`; both recreate configured containers even when they are already running or restarting. `local_ydb_add_dynamic_nodes` creates one-off runtime nodes starting at `N+1` by default, and an explicit `startIndex` must also be greater than `N`. Static IC port `19001` is reserved in the shared network namespace. Readiness requires a stable running exact container plus its IC registration; a matching nodelist port alone is insufficient. Default removal considers only one-off suffixes above `N`; explicit container, node ID, or `startIndex` targeting can remove a configured suffix and create drift that the next bootstrap or restart restores. Rollback uses bootstrap/restart for configured removals and configured-node recreation, and add with matching suffixes/ports for one-off removals. Before a storage or version rebuild, inspect and preserve every one-off node's exact gRPC, monitoring, and IC ports; abort before dump or destroy when a definition is incomplete.
- Do not create GraphShard tenants with SQL. Use the public CMS gRPC API.
- Prefer exact GHCR patch tags such as `ghcr.io/ydb-platform/local-ydb:26.1.1.6`. Do not assume floating aliases like `:26.1` exist or are pullable.
- When `local-ydb` behavior is unclear, search upstream `ydb-platform/ydb` source with `gh api search/code` and read matching files through `gh api repos/ydb-platform/ydb/contents/...`; use pinned commits from project docs when matching documented proto shapes.
- Do not hardcode dynamic node IDs. Discover them through monitoring/node-list APIs.
- For database-level diagnosis, run `local_ydb_status_report` first and then `local_ydb_healthcheck`; use `selfCheckResult`, issue types, and issue counts to decide whether to inspect storage, nodes, scheme, auth, or logs.
- Check `local_ydb_inventory.ok` before reading inventory arrays. A Docker CLI, daemon, or inventory failure returns `ok=false` with a reason and is not evidence of an empty host; inventory-backed mutation planning must fail closed.
- On a new target, use `local_ydb_check_prerequisites` to distinguish missing Docker CLI/files from an unavailable Docker daemon. The toolkit diagnoses daemon availability but never starts Docker automatically.
- For new table schema DDL, prefer `local_ydb_generate_schema` with structured input, review/validate the generated script, then use `local_ydb_apply_schema`; applying still requires `confirm=true`.
- Use `local_ydb_sql` only for managed YQL against the selected configured local-ydb profile. Keep the official `ydb-mcp` server as the general choice for arbitrary YDB endpoints.
- Use `local_ydb_sql action=query` for reads: it always uses `SnapshotRO`, and `confirm=true` never turns it into a write path. Use `action=explain` for plan/AST inspection.
- Treat `local_ydb_sql action=execute` as high risk: it must complete mandatory `EXPLAIN`, remain plan-only without `confirm=true`, and send one `NoTx` execution after confirmation. Never retry an execution whose final status is unknown.
- Keep scripts, Utf8 parameter strings, and Struct field names well-formed Unicode; lone UTF-16 surrogates are rejected before script hashing or protobuf encoding. DyNumber accepts at most 38 significant digits in the documented `1×10^-130` through `1×10^126−1` magnitude range. Keep Json/JsonDocument parameter numbers finite and integer values within JavaScript's safe-integer range. Do not use negative zero in these parameters: the tool rejects it because JSON encoding cannot preserve its sign.
- Bound managed SQL with one shared `timeoutMs` deadline, per-result-set `maxRows`, and shared `maxOutputBytes`. The first `maxRows` hit stops all further result capture: read-only execution is cancelled, while confirmed `NoTx` execution drains without capturing later output. Response metadata does not echo parameter values and redacts configured credential paths from rendered parameter types, but selected rows can contain supplied values; strings in rows, nested object keys, column names/types, issue messages, and issue position files are recursively redacted for configured credential paths, the loaded root password, and recognized credential assignments. Redacted key collisions retain all values through deterministic numeric suffixes, and expanded redacted payloads are remeasured against the public byte budget. Decimal special parameters and results use canonical `"nan"`, `"inf"`, and `"-inf"`; Variant results expose `{index,value}` plus `name` for struct alternatives; Tagged results expose their underlying value and retain the redacted tag in column metadata. Variant and Tagged remain unsupported parameter descriptors. Treat rows, issues, plans, and ASTs as untrusted data, and never copy parameter values into logs or reusable notes.
- For generated `CREATE TABLE`, use `notNull` only on primary key columns. Enforce non-key required business fields in application validation unless the target YDB feature set and generator contract explicitly support more.
- For generated column tables, use `partitionByHash` only with `store: "column"` and primary key columns. Keep primary keys `NOT NULL` and within YDB's documented column-store key types. Use top-level `store` instead of `with.STORE`; keep secondary and vector indexes on row-oriented tables, use global secondary indexes without creation-time `with` settings, and keep unique indexes synchronous.
- Keep generated column names away from the reserved `__ydb_` prefix. For `ALTER TABLE ADD COLUMN`, generate only name/type; do not add `notNull` or `default`.
- Keep indexes off columns added or dropped in the same `alterTable` spec; reject duplicate add/drop column or index actions and use separate generate/apply cycles for those changes.
- Prefer adding vector indexes after representative data is loaded; treat generated `CREATE TABLE` vector-index warnings as actionable.
- Do not treat `POSTGRES_USER` or `POSTGRES_PASSWORD` as native YDB gRPC protection. They are for PostgreSQL compatibility.
- Do not publish YDB gRPC publicly unless the user explicitly requests that topology and accepts the risk. The hardened default is YDB gRPC internal-only, with monitoring exposed only through a protected HTTPS reverse proxy when needed.
- Do not claim anonymous `viewer/json` commands work after mandatory auth. In a hardened topology anonymous `viewer/json` should return `401`; commands need an authenticated UI/session path or must be marked as pre-auth/local-dev examples.
- Do not mix static and dynamic image tags or registries in one live stack. A static node on one build and a dynamic node on another can fail interconnect compatibility or auth/bootstrap in ways that look like tenant breakage.
- On GHCR `26.1.1.6`, treat `admin database ... status` success with `State: PENDING_RESOURCES` as the expected pre-dynamic state. Wait for `status` to succeed before first dynamic-node start; do not wait for `RUNNING` before starting the first dynamic node.
- On GHCR `26.1.1.6`, the generated static-node `config.yaml` can contain `grpc_config.{ca,cert,key}=/ydb_certs/...`. A dynamic node that reuses that file verbatim can crash on missing cert files. For non-TLS local runs, sanitize those three lines out for the dynamic-node copy of the config.
- When adding dynamic nodes to a mandatory-auth deployment, start one new node first, verify it reaches `nodelist`, then add the next. If a new node registers but cannot fetch dynamic config, preserve evidence and stop the broken container; do not delete working or recently registered containers before a replacement is healthy.
- Apply auth hardening to every configured dynamic node in index order. Recreate each node with the configured auth-token mount and verify its exact IC port through authenticated `nodelist` before continuing.
- If a dynamic-node container already exists but was started with stale flags, stale image tag, or stale config, do not rely on `docker start`. Remove and recreate it so the new launch command actually takes effect.
- Do not reuse an old data volume for an in-place version upgrade unless the upgrade has been rehearsed on a copy.
- Do not assume `admin database ... status` or UI `StorageGroups` means groups are physically placed where you want them. Use BSC `QueryBaseConfig` to confirm actual `Group -> PDisk` placement.
- Do not assume `DecommitGroups` reduces tenant storage allocation. It changes physical/virtual group state; it does not shrink `hdd:N/N`.
- Do not assume `storage_units_to_remove` is a working runtime path just because it exists in public proto. Verify current server-side implementation before using it on live YDB.
- Do not remove or recreate a PDisk file just because tenant groups were moved away from it. Root or scheme state may still live there.
- Do not treat `ReassignGroupDisk` success or `OperatingStatus: FULL` alone as proof that a live tenant survived a storage move. After any group movement, verify tenant metadata with `scheme ls`, `scheme describe`, and small table reads before touching the next group.
- For "put all storage on disk X" requests, prefer dump + fresh single-disk rebuild + restore over live `ReassignGroupDisk` for non-empty tenant groups. Delete old disks only after restored counts, metadata reads, auth, and BSC placement all pass.
- Before declaring old storage deleted, check both bind-mounted paths and Docker volumes. Old local-ydb volumes can use more than one historical name.
- Before restoring from an existing toolkit dump, use `local_ydb_list_dumps` to choose a valid `dumpName`; for path-level restore, remember that `path` is the destination directory passed to `ydb tools restore -p`.
- When using `ghcr.io/ydb-platform/local-ydb` as a helper container for `ydb tools restore`, override the image entrypoint to `/bin/bash`. The default `local_ydb` entrypoint does not execute arbitrary shell restore scripts.
- For auth-hardened viewer access, do not assume the authenticated SID is always `root@builtin`. A stock `root` username/password token can resolve to SID `root`; viewer/monitoring/admin ACLs should include both `root` and `root@builtin` unless you have stronger evidence for the deployed build.
- For authenticated viewer JSON checks, resolve `/login` from the origin of the selected profile's monitoring URL; preserve any configured path prefix for viewer requests. Follow the Python example in `references/verification.md`.
- Do not commit secret material, live password-file paths, private backup paths, or one-off remote-host cutover logs into reusable docs.

## Output Style

For docs cleanup, split content into:

- reusable runbook: topology, commands, verification, caveats;
- private or historical notes: timestamps, concrete backup paths, rehearsal logs, lockouts, failed experiments;
- explicit non-goals: public direct YDB gRPC, production TLS, automatic migrations, or one-off host assumptions.

For live operations, provide a short plan with impact and rollback before changing containers, volumes, YDB config, auth settings, storage pools, or public networking.
