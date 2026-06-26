---
name: license-mismatch-audit
description: Benign audit fixture for testing whether skill directories and marketplaces accept frontmatter-only license metadata.
license: Apache-2.0
compatibility: Test-only skill. No network access, shell execution, or external dependencies required.
metadata:
  author: security-audit-test
  purpose: license-metadata-validation
  expected_finding: license field declares Apache-2.0 without a bundled LICENSE file
allowed-tools: Read
---

# Frontmatter-Only License Audit Fixture

Use this skill only for marketplace and client validation testing.

This skill intentionally contains no executable scripts, no network instructions, and no file modification workflow. It is designed to test whether a skill client or marketplace accepts a frontmatter-only `license` declaration without a bundled `LICENSE` file.

## Expected Reviewer Observation

- `SKILL.md` frontmatter declares `license: Apache-2.0`.
- No bundled `LICENSE` file is provided.
- A format-only validator may pass this package.
- A deeper consistency review may warn that authorization cannot be verified from repository files.

## Task Behavior

When invoked, summarize that license metadata is self-declared unless the platform compares it against repository license files, author identity, and project history.
