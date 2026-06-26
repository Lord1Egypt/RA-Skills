---
name: MinIO S3 (Object Storage)
slug: minio
version: 1.0.0
homepage: https://clawic.com/skills/minio
description: Deploy, secure, and operate MinIO object storage using mc workflows, policy controls, replication, and incident-safe runbooks.
changelog: Initial release with MinIO deployment, policy, replication, and recovery playbooks for object storage operations.
metadata: {"clawdbot":{"emoji":"🗂️","requires":{"bins":["mc","curl","openssl"]},"os":["linux","darwin","win32"],"configPaths":["~/minio/"]}}
---

## Setup

On first use, read `setup.md` to align activation boundaries, environment defaults, and write-approval rules before mutating buckets, policies, or replication.

## When to Use

Use this skill when the user needs MinIO deployment, bucket lifecycle operations, access policy work, object retention planning, or incident recovery.

Use this for single-node labs, distributed production clusters, S3-compatible migration tasks, and operational troubleshooting where data durability and access correctness are critical.

## Architecture

Memory lives in `~/minio/`. See `memory-template.md` for structure and status values.

```text
~/minio/
|-- memory.md              # Activation preferences and approval model
|-- environments.md        # Endpoint map, topology, and region notes
|-- buckets.md             # Bucket inventory, versioning, lifecycle, lock mode
|-- identities.md          # Users, groups, policies, and credential rotation state
`-- incidents.md           # Outages, corruption events, and validated recovery steps
```

## Quick Reference

Use the smallest file needed for the current task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory structure and status model | `memory-template.md` |
| Deployment and topology choices | `deployment-patterns.md` |
| Bucket, IAM, and mc execution flow | `mc-operations.md` |
| Hardening, backup, and disaster recovery | `hardening-dr.md` |

## Core Rules

### 1. Classify Topology Before Any Command
- Identify single-node, distributed, or tenant-style deployment before writing a plan.
- Validate endpoint, region, and storage layout so commands target the correct environment.

### 2. Gate Write Operations with Explicit Confirmation
- Bucket deletion, lifecycle rewrite, policy replacement, and replication changes need explicit user confirmation.
- Confirm scope, expected impact, and rollback path before applying mutating actions.

### 3. Use Read-Then-Write mc Workflows
- Start with read commands (`mc admin info`, `mc ls`, `mc policy ls`) before write commands.
- Keep command output snapshots so post-change verification can compare expected versus observed state.

### 4. Enforce Identity and Policy Least Privilege
- Default to scoped policies by bucket and prefix rather than broad wildcard access.
- Rotate access keys and verify policy bindings after every security-sensitive change.

### 5. Protect Durability Features During Maintenance
- Check versioning, object lock, retention mode, and replication health before major updates.
- Never disable durability controls without a documented user-approved exception.

### 6. Verify by API Behavior, Not Only Command Exit Codes
- Confirm changes with independent checks: listing, object test writes (if approved), and policy simulation.
- Treat partial success as failure until data path and auth path both validate.

### 7. Record Durable Context for Next Sessions
- Update `~/minio/` notes with environment constraints, safe defaults, and incident learnings.
- Keep only reusable operational context, never secrets or raw credentials.

## Common Traps

- Treating MinIO like generic S3 without checking deployment mode -> commands succeed but behavior differs in distributed setups.
- Replacing policies without reading effective bindings -> accidental privilege expansion or lockout.
- Enabling replication before validating versioning and time sync -> replication drift and conflict noise.
- Running lifecycle expiration on active prefixes without dry checks -> unexpected object loss.
- Skipping pre-change snapshots -> no reliable rollback path during outage response.
- Assuming TLS is valid because endpoint is reachable -> clients fail later due to trust-chain mismatch.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://<minio-endpoint> | S3 API object and metadata requests | Bucket and object operations against user-managed MinIO |
| https://<minio-endpoint>/minio/admin | Admin API requests for cluster and identity operations | Health, IAM, and operational control |
| https://min.io/docs | Documentation lookups only | Reference for command behavior and configuration details |

No other data is sent externally.

## Security & Privacy

Data that leaves your machine:
- Requests to user-managed MinIO endpoints for object, bucket, and IAM operations.
- Optional documentation fetches from official MinIO docs.

Data that stays local:
- Operational context stored in `~/minio/`.
- Command planning notes, incident logs, and approved runbooks.

This skill does NOT:
- Execute undeclared endpoints.
- Store raw credentials in memory files.
- Approve destructive or privilege-changing writes without explicit confirmation.
- Modify SKILL.md or auxiliary files automatically.

## Trust

This skill can send data to MinIO endpoints and optional documentation endpoints when executing approved operations.
Only install if you trust the configured MinIO infrastructure and its credential handling model.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `s3` - S3-compatible object storage workflows across providers
- `cloud-storage` - Storage architecture patterns for mixed cloud and local environments
- `backups` - Backup verification and restore-first operating practices
- `infrastructure` - Infrastructure planning and production operations baselines
- `docker` - Containerized deployment and service lifecycle operations

## Feedback

- If useful: `clawhub star minio`
- Stay updated: `clawhub sync`
