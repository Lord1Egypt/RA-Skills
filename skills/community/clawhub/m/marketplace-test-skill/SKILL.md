---
name: marketplace-test-skill
description: This skill should be used when turning raw commits, merged pull requests, issue lists, or plain change notes into concise user-facing release notes.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/qdw497874677/test-skill
    emoji: "N"
---

# Release Note Drafter

## Overview

Turn messy implementation details into release notes that users can understand. Prefer outcomes, behavior changes, and migration impact over internal file names, ticket IDs, or commit mechanics.

## Workflow

1. Identify the audience: end users, developers, operators, or internal stakeholders.
2. Group raw changes into `Added`, `Changed`, `Fixed`, `Removed`, `Security`, or `Internal` only when those categories are useful.
3. Rewrite each item as a user-visible outcome. Start with the benefit or changed behavior, not the implementation detail.
4. Merge duplicate or near-duplicate changes into one note.
5. Keep internal-only changes out of user-facing notes unless they affect reliability, security, performance, compatibility, or operations.
6. Add a `Migration Notes` section only when users must take action.
7. Add a `Known Issues` section only when limitations are explicitly provided.

## Expected Output

Return one of these formats based on the input size.

For small change sets:

```text
## Release Notes

- Added ...
- Fixed ...
- Changed ...
```

For larger releases:

```text
## Release Notes

### Added
- ...

### Changed
- ...

### Fixed
- ...

### Migration Notes
- ...
```

## Style Rules

- Use direct, plain language.
- Prefer active voice.
- Keep bullets short: one sentence when possible.
- Remove low-signal prefixes such as `feat:`, `fix:`, `chore:`, ticket IDs, and branch names.
- Avoid promising impact that is not present in the source material.
- Preserve breaking changes, deprecations, security fixes, data migrations, and required user actions.

## Resources

Read `references/release-note-style-guide.md` for examples, rewrite patterns, and category guidance.
