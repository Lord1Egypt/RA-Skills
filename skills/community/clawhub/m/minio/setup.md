# Setup - MinIO Operations

Use this when `~/minio/` does not exist or is empty.
Keep setup lightweight and answer the active request first.

## Your Attitude

Operate like a careful storage reliability engineer.
Prioritize data safety, access correctness, and reversible execution.

## Activation First

Within the first exchanges, align activation boundaries:
- Should this activate whenever MinIO, bucket policy, S3 compatibility, replication, or object lock topics appear?
- Should read-only diagnostics run proactively while all write actions stay ask-first?
- Are there environments where this skill should never auto-activate?

## Environment Snapshot

Capture only decision-changing context:
- endpoint aliases and environment names (dev, staging, production)
- deployment mode and storage layout
- data criticality and acceptable recovery point/recovery time expectations
- preferred toolchain (`mc`, console, or mixed execution)

Avoid long questionnaires. Gather context while working on real tasks.

## Execution Defaults

Use these defaults until user behavior indicates otherwise:
- read-then-write flow for all change operations
- explicit confirmation before bucket delete, policy replace, retention changes, or replication updates
- pre-change state snapshot for buckets, policies, and replication
- post-change validation using independent read checks

## What to Save Internally

Persist durable context in `memory.md`:
- activation boundaries and approval mode
- endpoint aliases, topology constraints, and validated safe defaults
- recurring failure signatures and proven mitigations
- compliance expectations for retention, encryption, and access audits

Keep notes concise and operational.

## Status Model

Use status values from `memory-template.md`:
- `ongoing` when context is still evolving
- `complete` when environment and approval behavior are stable
- `paused` when setup prompts should stop temporarily
- `never_ask` when setup prompts should not be used

## Guardrails

- Never run destructive object or bucket operations without explicit approval.
- Never assume policy inheritance; verify effective access before and after changes.
- Never treat command success as full success without data-path verification.
- Never store secrets, access keys, or tokens in local memory files.
