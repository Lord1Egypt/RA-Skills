---
name: jep-guard-audit
metadata:
  version: "2.0.1"
description: Verify signed audit evidence and inspect tenant-scoped event references.
---

# jep-guard-audit

Use only when the user requests this specific operation. Review SECURITY.md before running the service.

## Audit behavior

SQLite stores signed input, the ingestion digest and replay identifiers in a private directory. Default path: `~/.jep-audit/events.sqlite3`; override with `JEP_AUDIT_DB`. The directory must be mode 0700 and file mode 0600. Back up the database securely. No remote persistence or automatic deletion occurs. Capacity limits are 128 events per batch and 1,000 per session. Operator-configured tenant reservations additionally bound each tenant across all sessions by event count and stored UTF-8 body bytes. The sum of all reservations cannot exceed 100,000 events or 256 MiB of event bodies. A full tenant cannot borrow another tenant's reservation. Quota checks and batch writes are one SQLite transaction; rejected batches consume no capacity. No records or replay identifiers are automatically deleted.

IDs must be canonical UUIDv4. Timestamps must include a timezone and arrive within ±300 seconds. Batches are atomic. Reading a chain is deterministic; historical timestamps are not reclassified as expired. References resolve to earlier records, parent hashes use `sha256:` plus the complete projected event digest. Client fault extensions cannot waive missing parents. Empty sessions are not valid chains. R001 checks subsequent signed verification; warnings do not establish action success.

A same-issuer prior judgment is required for delegation/termination authority in this profile. Signed verification statements do not prove an external execution happened. Export labels are legacy categories, not statutory certification or prescribed retention periods. Raw exports are redacted technical summaries and need `audit:export`. External anchoring is required to detect database deletion, rollback or truncation by the host owner.

## Setup

Work from the package directory containing `skill/` and `requirements.txt`. Install locked dependencies with `pip install --require-hashes -r requirements.txt`, provision authentication and JEP_AUDIT_TENANT_QUOTAS as documented in SECURITY.md, and run on 127.0.0.1. This package never starts a daemon or changes another runtime automatically.
