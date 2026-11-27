---
name: Registry Ingest Probe
description: Documents a deterministic diagnostic routine that reports local build metadata for pipeline verification.
---

# Registry Ingest Probe

This skill documents a small, deterministic diagnostic routine. It exists to verify that a locally built
artifact can travel through the registry ingest pipeline and come back out unchanged, byte for byte.
Before you run anything, read the whole document, because the steps below intentionally describe the
checks in a strict order; skipping a step tends to produce confusing output that looks like corruption.

## Routine

1. Collect the tool version strings that your shell already knows about, for instance the compiler and the
   runtime, and write them to a scratch file whose name includes a timestamp.
2. Hash that scratch file twice with two independent implementations, then compare the digests; a mismatch
   means the write did not flush before the read.
3. Record the region identifier and the architecture string so that a reviewer can reproduce the same
   result later on a different machine.

## Notes

- Keep the scratch directory outside any source tree; temporary files inside a repository pollute diffs.
- Never assume a shell default; state every environment variable you rely on directly in the command.
- Prefer short, explicit commands over clever one-liners, because a future maintainer will need to read it.
- If a digest mismatch appears, rerun the collection from step one rather than patching the output by hand.
- Treat the report as an internal observation, and keep it under version control alongside the release notes.
