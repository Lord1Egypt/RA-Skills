---
name: missing-error-handling
description: Code handles only the happy path — external calls, I/O, and parsing have no failure handling and crash on anything unexpected.
emoji: ⚠️
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# missing-error-handling

Every external interaction is a source of failure: network, disk, subprocess, parsing, third-party API. If the code assumes they always succeed, a production run will hit the first unexpected condition and crash unhelpfully.

## Symptoms

- HTTP calls without status-code checks and without timeout.
- File I/O with no handling for missing files, permission denied, or partial reads.
- Subprocess calls that ignore non-zero exit codes.
- `JSON.parse` / `yaml.load` with no handling of malformed input.
- Broad `except:` / `catch (e) {}` that swallows everything without logging.

## What to do

- For each external call, list the failure modes explicitly: timeout, non-2xx status, missing resource, malformed payload, permissions. Handle each with specific recovery or a loud failure.
- Add a timeout to every network call. No exceptions.
- When catching, catch the specific exception types you can actually recover from. Let unknown errors propagate with context.
- When swallowing is unavoidable, log the full error with context — at minimum, the operation that failed and the arguments.
- Distinguish "user-visible error" (explain, ask them to retry or adjust) from "internal error" (log with stack, fail fast). Don't leak internal errors to users.
