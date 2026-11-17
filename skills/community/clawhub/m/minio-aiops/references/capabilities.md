# minio-aiops capabilities

> 48 MCP tools (28 read, 18 write, 2 undo) over four access paths:
> the **S3 API** (official SDK, SigV4), the **admin API**, the unauthenticated
> **health endpoints**, and the **cluster metrics endpoint**.

## Health (read)

| Tool | Surface | Returns |
|------|---------|---------|
| `health_live` | `GET /minio/health/live` | node liveness (reachable/healthy/status code) |
| `health_ready` | `GET /minio/health/ready` | node readiness |
| `health_cluster` | `GET /minio/health/cluster` | write-quorum health (503 = degraded) + live/ready + overall verdict |
| `cluster_status` | metrics endpoint | nodes/drives online+offline, raw/usable capacity, buckets, objects |
| `fleet_overview` | composite | health + capacity headline + exposure headline in one call |

## Flagship analyses (read)

| Tool | Surface | Returns |
|------|---------|---------|
| `capacity_rca` | metrics endpoint | findings with **cause + suggestedAction**: CLUSTER_FULL / CLUSTER_NEARFULL / DRIVES_OFFLINE / NODES_OFFLINE / DRIVE_HOTSPOT / DRIVE_IMBALANCE; per-drive usage table |
| `usage_by_bucket` | metrics endpoint | envelope `{buckets, returned, limit, truncated}` — per-bucket bytes + objects, biggest first |
| `healing_health` | metrics endpoint | per-erasure-set online drives / write quorum / **failureToleranceRemaining**, healing drives, heal backlog + errors; findings WRITE_QUORUM_LOST / _AT_EDGE / LOW_FAILURE_TOLERANCE / HEALING_IN_PROGRESS / HEAL_ERRORS / HEALING_STATUS_UNKNOWN / ERASURE_SETS_UNREAD; an unscraped gauge is `null` (and `healthy: null` when no erasure-set data was read), never 0 |
| `drive_status` | metrics endpoint | per-drive rows (server, drive, used ratio), fullest first |
| `node_status` | metrics endpoint | nodes online/offline + per-node drive counts |
| `bucket_exposure_audit` | S3 API per bucket | reports `bucketsAudited`/`bucketsTotal`/`truncated`; **ranked** findings: PUBLIC_WRITE_POLICY / PUBLIC_READ_POLICY / NO_DEFAULT_ENCRYPTION / VERSIONING_OFF / NO_LIFECYCLE with riskScore + riskLevel |
| `lifecycle_gap_analysis` | S3 API + metrics | reports `bucketsAnalyzed`/`bucketsTotal`/`truncated`; gaps: NONCURRENT_VERSIONS_UNBOUNDED (+reclaimable estimate) / INCOMPLETE_UPLOADS_NO_ABORT_RULE (+counts, ages) / NO_LIFECYCLE_ON_LARGE_BUCKET |
| `diagnose_retention_gaps` | S3 API per bucket | envelope `{findings, returned, limit, truncated}` + `bucketErrors`; worst-first with `rank`: LIFECYCLE_CANNOT_EXPIRE_UNDER_RETENTION (both day counts + shortfall) / LOCK_ENABLED_NO_DEFAULT_RETENTION / LOCK_WITHOUT_ACTIVE_VERSIONING / COMPLIANCE_DEFAULT_LONG / GOVERNANCE_DEFAULT_BYPASSABLE |

## Buckets (read)

| Tool | Surface | Returns |
|------|---------|---------|
| `bucket_ls` | `ListBuckets` | envelope `{buckets, returned, limit, truncated}` — name + creation time (`createdAt` is `null`, not `""`, when absent) |
| `bucket_info` | composite per bucket | policy (present/publicRead/publicWrite), versioning, lifecycle rules, encryption, quota, tags — per-probe failures degrade to an `errors` list |
| `bucket_policy_get` | `GetBucketPolicy` | verbatim policy JSON + anonymous-access summary |
| `bucket_lifecycle_get` | `GetBucketLifecycle` | rules as dicts (ruleId, status, prefix, expirationDays, noncurrentExpirationDays, abortIncompleteDays) |
| `bucket_versioning_get` | `GetBucketVersioning` | Enabled / Suspended / Off |
| `bucket_quota_get` | admin API | hard quota bytes (0 = unlimited) |
| `object_ls` | `ListObjectsV2` | envelope `{objects, returned, limit, truncated}` — bounded listing (default 100, max 1000) under a prefix; `truncated` is **measured** (one row over-fetched); `lastModified`/`versionId` are `null` when absent |
| `incomplete_uploads_ls` | `ListMultipartUploads` | envelope `{uploads, returned, limit, truncated}` — object, uploadId, initiated time (`null` when absent) |
| `server_info` | admin API | mode, deployment id, server/pool counts |

## Object lock / WORM (read)

| Tool | Returns |
|------|---------|
| `bucket_lock_config` | `objectLockEnabled` + `defaultRetention` (+ `defaultRetentionDays`, years converted) + `versioning`. **Keeps two absences apart**: `objectLockEnabled: false` (lock was never enabled and S3 accepts the flag only at bucket creation, so it never can be) vs `true` with `defaultRetention: null` (WORM available, but an upload omitting its own retention header is retained for nothing) |
| `object_lock_status` | one version's `retention` + `legalHold` + `retentionDaysRemaining`, plus `protection`: `versionDestroyable`, `blockedBy` (they stack), `bypassable`, and `deleteMarkerStillPossible` — a plain DELETE always succeeds on a versioned bucket and hides the key while the retained version survives |

## Writes (governed; all take `dry_run`)

| Tool | Risk | Undo | Notes |
|------|:----:|:----:|-------|
| `set_bucket_policy` | medium | prior policy JSON (or delete if none) | policy_json validated as JSON with a Statement |
| `delete_bucket_policy` | medium | re-apply prior policy JSON | no-op undo when there was none |
| `set_versioning` | medium | prior state | prior "Off" undoes to Suspended (S3 cannot return to Off — noted) |
| `set_lifecycle` | medium | prior lifecycle XML (or delete if none) | day-count knobs build rules; `lifecycle_xml` applies verbatim (undo path) |
| `delete_lifecycle` | medium | re-apply prior lifecycle XML | |
| `set_bucket_quota` | medium | prior quota (0 clears) | admin API |
| `bucket_delete` | **high** | none (irreversible) | refused unless verifiably empty (versions + delete markers included); priorState = bucket meta |
| `remove_incomplete_uploads` | medium | none (parts unrecoverable) | age-gated (default: only uploads ≥ 7 days old); priorState = count + sample |
| `bucket_create` | medium | delete the bucket (empty-only) | `object_lock=True` is the ONLY route to a WORM-capable bucket; reports lock + versioning as **observed**, not echoed |
| `set_default_retention` | **high** | prior default rule (or clear) | applies to future uploads only; undo restores the rule, objects written under it keep their own retention |
| `clear_default_retention` | medium | prior default rule | clears the rule only — object lock stays enabled (S3 has no call that disables it) |
| `set_legal_hold` | medium | prior hold state | the one WORM control reversible by design; stacks with retention |
| `set_object_retention` | **critical** | **none, and none is possible** | extend-only: shortening/downgrading is refused locally because S3 needs `x-amz-bypass-governance-retention`, which the minio SDK never sends. COMPLIANCE additionally needs `acknowledge_irreversible=True`. Verified on a live MinIO: root with `--bypass` could not clear, downgrade, or version-delete a COMPLIANCE object |

## Out of scope

- Site replication status/management
- IAM **policy authoring** (creating/editing policy documents; attaching existing
  ones is supported) and group-membership writes
- Tiering to remote storage

Missing something you need? **Open an issue or send a PR** — feedback welcome.

## Authorization

There is no read-only switch, policy file, or approval gate. Whether a write is
permitted is the agent's decision or the permission of the access key you
connect with (a read-only IAM policy makes writes fail at the server). Every
call — read or write, MCP or CLI — is audited. See `agent-guardrails.md`.
