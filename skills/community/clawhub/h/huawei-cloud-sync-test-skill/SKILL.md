---
name: huawei-cloud-sync-test-skill
description: |
  A test skill for the multi-repo sync pipeline. It documents the expected flow:
  GitCode master squash merge -> filtered github branch -> GitHub mirror, GitCode
  mirror (rewritten authors) and ClawHub publish. This skill has no scripts; it
  exists only to trigger and verify an end-to-end sync and is safe to remove.
---

# huawei-cloud-sync-test-skill

Purpose

This skill is used to exercise the repository mirror sync pipeline. It contains
only documentation and no executable code.

## Expected pipeline behaviour

1. A squash merge to `master` becomes one commit on `master`.
2. The commit is replayed onto the `github` branch (excluding configured paths).
3. Both git mirrors receive a DAG-preserving copy with rewritten authors.
4. ClawHub publishes this skill under the configured owner.

## Notes

- Safe to delete after verification.
- Not intended for production use.
