# permission-manifest-guard

An OpenClaw skill that inspects skill directories before install or execution, produces a human-readable permission manifest, and recommends disposition when declared metadata does not match observed behaviour.

## Overview

permission-manifest-guard statically analyses an OpenClaw skill directory and extracts permission-relevant signals:

- Required binaries and CLIs
- Shell commands and subprocess usage
- Network domains and URLs
- File paths read or written
- Config files expected
- Environment variables and secrets
- Package manager and dependency install behaviour
- Risky capabilities

It produces a **Markdown manifest**, a **JSON manifest**, and a **disposition recommendation** (review, sandbox, or reject).

## Usage

Point the skill at an OpenClaw skill directory. It reads `SKILL.md`, source files, and configuration to build its analysis.

When invoked via the CLI (`npx permission-manifest-guard /path/to/skill`), the tool writes `permission-manifest.json` into the target directory as a side effect. The programmatic API (`analyzeSkill()`) returns results in memory and does not write any files.

## Trade-offs

- **Static analysis only** — no runtime instrumentation. This means the skill cannot detect dynamically constructed shell commands or lazily loaded dependencies that are not visible in source.
- **Conservative by default** — the skill may over-flag rather than under-flag. This trades false positives for safety but may require manual review of flagged items.
- **Keyword-based detection** — pattern matching on source text is fast but can produce false positives from comments, string literals, or dead code paths.

## Limitations

- Does not execute the target skill or any of its code.
- Cannot detect obfuscated or encrypted payloads.
- Depends on file-system patterns that may not cover every language or framework.
- Does not verify network reachability or validate URLs.

## Non-goals

- Runtime sandboxing or process isolation — this skill only recommends, it does not enforce.
- Signature verification or cryptographic integrity checks.
- Dependency vulnerability scanning (use dedicated tools for CVE checks).
- Modifying or patching the inspected skill.
