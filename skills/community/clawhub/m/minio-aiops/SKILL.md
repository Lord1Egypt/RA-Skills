---
name: minio-aiops
slug: minio-aiops
displayName: "MinIO AIops"
summary: "Governed MinIO ops: capacity RCA, exposure audit, ILM, WORM retention, IAM, healing, 48 tools."
license: MIT
homepage: https://github.com/AIops-tools/MinIO-AIops
tags: [aiops, mcp, governance, minio]
description: >
  Use this skill whenever the user needs to operate or diagnose MinIO object storage — explain why the cluster is filling up or refusing writes (capacity_rca), find publicly exposed buckets and hygiene gaps (bucket_exposure_audit), find storage that lifecycle/ILM should be reclaiming but isn't, including noncurrent versions and incomplete multipart uploads (lifecycle_gap_analysis), check heal backlog and erasure-set write-quorum risk (healing_health), read service health / cluster status / per-bucket config (policy, versioning, lifecycle, encryption, quota, tags) — plus governed writes (set or delete bucket policy, enable/suspend versioning, set or delete lifecycle rules, set bucket quota, purge incomplete uploads, delete an empty bucket).
  Always use this skill for "minio health", "why is my object storage full", "which bucket is biggest", "is any bucket public / anonymous access", "versioning / noncurrent versions piling up", "incomplete multipart uploads", "lifecycle / ILM rules", "bucket quota", "erasure set / drive failure tolerance", "healing backlog", or "delete a bucket safely" when the context is a MinIO deployment.
  Do NOT use when the target is not MinIO — for Ceph/RGW use ceph-aiops; for TrueNAS storage use truenas-aiops; for a hypervisor, backup product, container cluster, or network device route to the appropriate other AIops-tools skill (negative routing hint only).
  Common MinIO ops with a built-in governance harness (audit, policy, token budget, undo, risk-tiers).
installer:
  kind: uv
  package: minio-aiops
argument-hint: "[minio question or describe your object-storage task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["minio-aiops","uvx"]},"optional":{"env":["MINIO_AIOPS_CONFIG","MINIO_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/MinIO-AIops","emoji":"🪣","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed MinIO operations. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency. Works against any reasonably current MinIO server (single-node or distributed/erasure-coded); admin features (quota, server info) need admin-capable keys.
  All write operations are audited to a local SQLite DB under ~/.minio-aiops/ (relocatable via MINIO_AIOPS_HOME).
  Connection: the S3 API endpoint (host:port, default 9000; SigV4 via the official SDK), plus the unauthenticated health endpoints (/minio/health/live|ready|cluster) and the cluster metrics endpoint (/minio/v2/metrics/cluster — public mode or the default bearer-token mode; the token is derived from the stored credentials, no extra secret). The access key lives in config.yaml; the secret key is stored ENCRYPTED in ~/.minio-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'minio-aiops init' to onboard, or 'minio-aiops secret set <target>' to add one. The store is unlocked by a master password from MINIO_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var MINIO_<TARGET_NAME_UPPER>_SECRET_KEY is still honoured as a fallback with a deprecation warning (migrate with 'minio-aiops secret migrate'). Secrets are held only in memory, never logged or echoed.
  State-changing operations require double confirmation at the CLI layer and support --dry-run. All write tools pass through the @governed_tool decorator (budget guard + audit + undo + risk-tier labelling). bucket_delete is high-risk, dry-run + double-confirm, and refused unless the bucket is verifiably empty (including versions and delete markers); remove_incomplete_uploads only aborts uploads older than a safety window. Reversible writes (set/delete bucket policy, set_versioning, set/delete lifecycle, set_bucket_quota) capture the prior state and record an inverse undo descriptor.
  Webhooks: none — no outbound network calls beyond the configured MinIO endpoint.
  SSL: secure (https) and verify_ssl default to true; disable verification only for self-signed lab certificates.
  Transitive dependencies: the official minio SDK, httpx, and the MCP SDK. No post-install scripts or background services.
  Verification status: validated against mocked SDK/HTTP responses; no recorded end-to-end run against a live MinIO server yet. Erasure-set/healing findings need a multi-drive deployment to observe live (a single-node server running 'minio-aiops doctor' is the cheapest live path). See docs/VERIFICATION.md.
---

# MinIO AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by MinIO, Inc. or any storage vendor.** Product and trademark names belong to their owners. Source at [github.com/AIops-tools/MinIO-AIops](https://github.com/AIops-tools/MinIO-AIops) under the MIT license.

Governed MinIO object-storage operations — **48 MCP tools**, every one wrapped with the bundled `@governed_tool` harness: a local unified audit log under `~/.minio-aiops/`, a token/runaway budget guard, undo-token recording, and a descriptive risk tier on every audit row. The secret key is stored **encrypted** (`~/.minio-aiops/secrets.enc`, Fernet + scrypt) — never plaintext on disk. Six flagship analyses turn raw state into plain-language **cause + suggested action**: `capacity_rca`, `bucket_exposure_audit`, `lifecycle_gap_analysis`, `healing_health`, `diagnose_retention_gaps`, `diagnose_iam_exposure`.

> **Standalone**: the governance harness is bundled in the package (`minio_aiops.governance`) — minio-aiops has no external skill-family dependency. Verification status and the live-run checklist are in `docs/VERIFICATION.md`.

> **Authorization is not this tool's job**: whether a write is permitted is the agent's judgement or the permission of the access key you connect with (a read-only IAM policy makes writes fail at the server). There is no read-only switch, policy file, or approval gate — the guarantee is that every call is audited. Driving this with a smaller / local model? See `references/agent-guardrails.md`.

## What This Skill Does

| Group | Tools | Count | Read or Write |
|-------|-------|:-----:|:-------------:|
| **Health** | health_live, health_ready, health_cluster, cluster_status, fleet_overview | 5 | 5 read |
| **Capacity** | capacity_rca (flagship), usage_by_bucket | 2 | 2 read |
| **Healing** | healing_health (flagship), drive_status, node_status | 3 | 3 read |
| **Exposure / ILM** | bucket_exposure_audit (flagship), lifecycle_gap_analysis (flagship) | 2 | 2 read |
| **Buckets** | bucket_ls, bucket_info, bucket_policy_get, bucket_lifecycle_get, bucket_versioning_get, bucket_quota_get, object_ls, incomplete_uploads_ls, server_info | 9 | 9 read |
| **Writes** | set_bucket_policy, delete_bucket_policy, set_versioning, set_lifecycle, delete_lifecycle, set_bucket_quota, bucket_delete, remove_incomplete_uploads | 8 | 8 write |
| **Object lock (WORM)** | bucket_lock_config, object_lock_status, diagnose_retention_gaps (flagship) | 3 | 3 read |
| | bucket_create, set_default_retention, clear_default_retention, set_legal_hold, set_object_retention | 5 | 5 write |
| **IAM** | iam_users, iam_groups, iam_policies, diagnose_iam_exposure (flagship) | 4 | 4 read |
| | create_user, set_user_status, remove_user, attach_user_policy, detach_user_policy | 5 | 5 write |
| **Undo** | undo_list, undo_apply | 2 | read + replay |

Totals: **48 tools — 28 read, 18 write, 2 undo.** The MCP server exposes all 48; the CLI is a convenience subset.

## Quick Install

```bash
uv tool install minio-aiops
minio-aiops init       # interactive wizard: endpoint + access key + encrypted secret key
minio-aiops doctor
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/minio-aiops
openclaw skills info minio-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- **"Storage is filling up / writes are failing"** → `capacity_rca` (capacity vs used, offline drives/nodes, hotspots — cause + action per finding), then `usage_by_bucket` for the biggest consumers
- **"Is anything exposed?"** → `bucket_exposure_audit` (ranked: public read/write policies, missing encryption, versioning off, no lifecycle)
- **"Where did my space go?"** → `lifecycle_gap_analysis` (unbounded noncurrent versions, incomplete multipart uploads, reclaimable estimate) then `remove_incomplete_uploads` + `set_lifecycle` to fix it for good
- **"How many more drives can fail?"** → `healing_health` (per-erasure-set online drives vs write quorum, heal backlog/errors)
- One-shot triage (`fleet_overview` / `minio-aiops overview`): health + capacity headline + exposure headline
- Per-bucket questions: `bucket_info` (policy/versioning/lifecycle/encryption/quota/tags in one answer)
- Safely change policy/versioning/lifecycle/quota (reversible, undo recorded) or delete an **empty** bucket (governed, dry-run + double confirm)

**Do NOT use when** the target is not MinIO — for Ceph/RGW use **ceph-aiops**; for TrueNAS use **truenas-aiops**; for a hypervisor, backup product, container cluster, or network device route to the appropriate **other AIops-tools** skill.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| MinIO: capacity RCA, bucket exposure, ILM gaps, healing, bucket writes | **minio-aiops** (this skill) |
| Ceph/RGW storage | **ceph-aiops** |
| TrueNAS storage appliances | **truenas-aiops** |
| Any other target (hypervisor, backup, cluster, network) | the appropriate **other AIops-tools** skill |

## Common Workflows

Each recipe starts from an RCA read and ends in a governed, reversible write.
Every write step accepts `--dry-run`; irreversible ones also double-confirm.

### 1. "Backups are failing — the cluster says it's out of space"

1. `minio-aiops overview` → one-shot triage: health + capacity headline + exposure headline.
2. `minio-aiops capacity rca` → ranked findings with cause + action (`CLUSTER_NEARFULL`, `DRIVES_OFFLINE`, `DRIVE_HOTSPOT`, …). Note which finding is actually driving the fill.
3. `minio-aiops capacity usage` → the biggest buckets, largest first, so you know where the bytes live.
4. `minio-aiops bucket ilm-gap` → how much of that is reclaimable: unbounded noncurrent versions and abandoned multipart uploads, with an estimate.
5. Reclaim the abandoned uploads: `minio-aiops bucket purge-uploads <bucket> --older-than-days 7 --dry-run`, then re-run without `--dry-run` (double confirm — this one is irreversible, only uploads older than the window are aborted).
6. Cap version growth: `minio-aiops bucket lifecycle-set <bucket> --noncurrent-days 30` (reversible — the prior lifecycle config is captured). Abandoned uploads have no server-side rule — MinIO does not honour a lifecycle abort-incomplete rule — so re-run `purge-uploads` periodically instead.
7. `minio-aiops capacity rca` again to confirm the finding cleared.

**Failure branch**: if `capacity rca` reports `DRIVES_OFFLINE` rather than genuine data growth, stop — do not delete anything. The space is not gone, it is unavailable. Go to recipe 3 and restore drive/erasure-set health first; purging data under a degraded erasure set removes redundancy you may need.

### 2. "Someone says one of our buckets is readable from the internet"

1. `minio-aiops bucket audit` → ranked exposure findings, riskiest first (`PUBLIC_WRITE_POLICY`, `PUBLIC_READ_POLICY`, missing encryption, versioning off, no lifecycle).
2. `minio-aiops bucket info <bucket>` → the full per-bucket picture (policy, versioning, lifecycle, encryption, quota, tags) so you fix the right thing.
3. Decide the fix. To remove anonymous access entirely: `minio-aiops bucket policy-set <bucket> --file restricted-policy.json --dry-run`, then re-run for real. To drop the policy altogether, use the `delete_bucket_policy` MCP tool. Both are reversible — the prior policy JSON is captured.
4. `minio-aiops undo list` → confirm an undo token was recorded for the change you just made.
5. `minio-aiops bucket audit` → confirm the finding is gone.

**Failure branch**: if the write is refused by the server with an access-denied error, the access key you connected with lacks permission for that operation — the tool does not gate the write, the key does. Connect with a key whose IAM policy allows it (or ask whoever owns the key). If the new policy breaks a legitimate consumer, `minio-aiops undo apply <id>` restores the exact prior policy document.

### 3. "A drive died — how many more failures can we take?"

1. `minio-aiops health check` and `minio-aiops health status` → is the cluster serving reads and writes at all right now?
2. `minio-aiops heal status` → per erasure set: online drives vs write quorum, `failureToleranceRemaining`, healing drives, heal backlog and errors.
3. `minio-aiops heal drives` → which specific drives are offline or healing.
4. `minio-aiops heal nodes` → whether the failures cluster on one node (a node problem, not a drive problem).
5. If `WRITE_QUORUM_AT_EDGE` appears, the next failure stops writes: replace drives before any maintenance, and re-run `heal status` until the backlog drains.

**Failure branch**: if the heal backlog is not shrinking between runs, do not start more maintenance. Check `heal nodes` for an offline node first — a down node makes its drives look like many simultaneous drive failures, and replacing hardware will not fix it.

### 4. "The auditor asked whether our retained data is actually protected"

1. `minio-aiops lock gaps` → ranked WORM findings across every bucket. The two that matter most: `LOCK_ENABLED_NO_DEFAULT_RETENTION` (the bucket advertises object lock but retains nothing unless each upload asks) and `LIFECYCLE_CANNOT_EXPIRE_UNDER_RETENTION` (an expiry rule that retention outlives, so the capacity never returns — both day counts are in the finding).
2. `minio-aiops lock config <bucket>` → whether object lock is enabled at all. `objectLockEnabled: false` is terminal: S3 accepts the flag only at bucket creation, so the answer is a new bucket plus a migration, not a setting.
3. `minio-aiops lock status <bucket> <key>` → for a specific object: retention mode, days remaining, legal hold, and `protection.versionDestroyable` with what is blocking it. Note `deleteMarkerStillPossible`: object lock protects the bytes, not the key's visibility.
4. Close the gap for future uploads: `minio-aiops lock default-set <bucket> GOVERNANCE --days 365 --dry-run`, then for real (reversible — the prior rule is captured).
5. `minio-aiops lock gaps` again → confirm the finding cleared, and check whether step 4 introduced the lifecycle contradiction from step 1.

**Failure branch**: `lock default-set` refused with "does not have object lock enabled" means the bucket can never be made WORM in place — create one with `minio-aiops lock bucket-create <new> --object-lock` and migrate. If the auditor requires retention nobody can lift, that is COMPLIANCE, not GOVERNANCE — and it is genuinely permanent: verified on a live server, root with `--bypass` could not clear it, downgrade it, or delete the version. `set_object_retention` therefore records **no undo token**, refuses any call that would shorten retention already in force, and requires `acknowledge_irreversible=True`. Use GOVERNANCE unless permanence is the actual requirement.

### 5. "Decommission a retired bucket"

1. `minio-aiops bucket ls` → confirm the exact bucket name.
2. `minio-aiops bucket info <bucket>` → verify it is genuinely retired (check versioning, lifecycle and quota, not just the object count).
3. `minio-aiops bucket uploads <bucket>` → surface incomplete multipart uploads, which keep a bucket non-empty even when it looks empty.
4. `minio-aiops bucket purge-uploads <bucket> --older-than-days 7` if any remain (dry-run first, double confirm).
5. `minio-aiops bucket delete <bucket> --dry-run` → shows the API call, changes nothing.
6. Re-run without `--dry-run`: double confirm, **high** risk. Execution re-checks emptiness (versions and delete markers included) and refuses otherwise — this tool never mass-deletes data.

**Failure branch**: if the delete is refused as non-empty, that is the guard doing its job — the bucket still holds objects, noncurrent versions, delete markers, or incomplete uploads. Go back to step 3, and never work around the guard by deleting data out-of-band; this tool deliberately has no mass-delete path.

## Governance & Safety

- The skill delivers reads and writes and records them; it does **not** decide whether a write is permitted — that is the agent's judgement or the permission of the access key you connect with (a read-only IAM policy makes writes fail at the server). There is no read-only switch, policy file, or approval gate.
- **Audit is the guarantee**: every tool — MCP and CLI alike — is audited to `~/.minio-aiops/audit.db` (relocatable via `MINIO_AIOPS_HOME`). `MINIO_AUDIT_APPROVED_BY` / `MINIO_AUDIT_RATIONALE` are optional annotations recorded when set, never required.
- The declared `risk_level` (`bucket_delete` is high) is carried into the audit row as a descriptive tier — a label for the reviewer, not a gate.
- Destructive writes support `--dry-run` and double confirmation at the CLI.
- Reversible writes record an inverse descriptor capturing the real prior state (policy JSON, lifecycle XML, versioning state, quota).

## References

- `references/capabilities.md` — full tool → API-surface → returns reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, and connectivity
