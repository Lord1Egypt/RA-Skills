# Stable Version Index — {{PROJECT_NAME}}

Tracks stable/released versions with human judgments. Each entry links to its
evidence (viewer, report, or test output) so versions can be compared and
rolled back.

## File Authority Levels

| Level | Meaning |
|---|---|
| AUTHORITATIVE | Current official version |
| STABLE | Verified, usable as a baseline |
| EXPERIMENTAL | In testing, not a default authority |
| HISTORICAL | Past artifacts, reference only |
| DEPRECATED | Replaced by something newer |
| ARCHIVED | Archived, not part of current work |

> **文件存在 ≠ 文件有效。** Only human-confirmed versions are marked stable.

| Version | Series | Stable? | Judge | Evidence link | Notes |
|---|---|---|---|---|---|
| {{VERSION}} | {{SERIES}} | yes/no | human/ai | {{LINK}} | {{NOTES}} |

## Rules

- Only human-confirmed versions are marked stable.
- Keep the previous version's entry when a new one supersedes it; mark it `superseded`.
- Link evidence using relative paths, not absolute paths.
