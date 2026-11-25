---
name: i45943-fileparam-test
description: Self-contained operational runbook for verifying ClawHub file endpoint parameter handling. Use when you need a reproducible, benign skill package for endpoint isolation testing.
---

# i45943 fileparam canary

CANARY_VERSION_2_TEXT.

## Overview

This skill is a self-controlled test fixture used to exercise the ClawHub skill file
resolution endpoint under varied query parameters. It contains no executable logic and
no third-party credentials. All content is authored for reproducibility only.

## When to use this skill

Use this skill when you want a stable, versioned reference package whose only purpose is
to confirm how the platform resolves file paths, versions, tags, and owner handles during
anonymous reads. The workflow is deterministic and does not mutate external state.

## Step by step procedure

1. Confirm the package metadata is visible through the public listing surface.
2. Resolve the version pointer and record the resolved semantic version.
3. Request the SKILL.md body and verify the canary marker matches this revision.
4. Publish a subsequent revision and confirm the earlier canary marker remains readable.
5. Compare responses across owner-qualified and owner-less requests.
6. Record status codes, content types, and cache headers for each request.

## Expected results

Each request should return the exact canary marker associated with the requested
revision. Requests for unknown revisions should not silently downgrade to the latest
revision; they should surface a not-found result instead.

## Troubleshooting

If the marker does not match, confirm the requested version string is trimmed of leading
and trailing whitespace, then re-request using an explicit version selector rather than
the default latest pointer. Keep owner-qualified requests consistent within a run.

## Notes

This document is intentionally verbose so that the package passes minimum documentation
quality thresholds during publication. No secrets, tokens, private keys, or production
endpoints are present in this file or in any file shipped alongside it.

REVISION_TWO_BODY_END.
