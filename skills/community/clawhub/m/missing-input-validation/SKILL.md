---
name: missing-input-validation
description: External input flows into sensitive operations without being checked for type, shape, range, or sanitization.
emoji: 🛡️
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# missing-input-validation

Any data from outside the process — HTTP request bodies, CLI args, file contents, third-party API responses, user messages — should be treated as untrusted until proven otherwise. Code that uses it directly opens injection, crash, and security paths.

## Symptoms

- HTTP handler uses `request.body.x` with no type check.
- CLI flag value passed straight into `exec`, `SQL`, or a file path.
- Third-party API response fields accessed without confirming they exist.
- Numeric input used in array indexing or arithmetic with no bounds check.
- String input concatenated into SQL, shell commands, or file paths.

## What to do

- At every trust boundary, validate type, shape, and range before using the value. Reject early with a clear error message.
- For structured payloads, use a schema validator (Zod, Pydantic, ArkType, etc.) — don't hand-write "if field exists".
- For values used in SQL, shell, or file paths, use parameterized queries, `execFile` with an argv array, or explicit path joins — never string concatenation.
- When an invariant is checked, include the unexpected value in the error so debugging is possible.
- Third-party responses are *not* trustworthy. Validate them the same way you'd validate user input.
