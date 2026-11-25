## Summary

Fixes #<issue-number>.

One or two sentences on what changed and why.

## Root cause

What was wrong, and where. Link the file and function.

## Reproduction

Before the fix:

```bash
<command>
```

Result: failed with `<short error or assertion>`.

After the fix:

```bash
<command>
```

Result: passed.

## Changes

- `path/to/file`: what changed and why.
- `path/to/test`: what the new test proves.

## Verification

| Check | Command | Result |
| --- | --- | --- |
| Focused test | `<command>` | `N passed` |
| Red-green proof | `<command>` with the source change removed | failed as expected |
| Package tests | `<command>` | `N passed` |
| Types | `<command>` | passed |
| Lint | `<command>` | passed |
| Full suite | `<command>` | `N passed`; pre-existing failures: `<list or none>` |

## Risk and rollback

- Risk: Low / Medium / High — reason.
- Rollback: revert `<commit>`; no data or migration changes.

## Not covered

- What this PR intentionally leaves out, and why.
- Follow-up issues or known gaps.

## Screenshots

For UI changes only: before/after screenshots or a short recording.
