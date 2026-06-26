# Security Policy

## Purpose

This is a **read-only metadata utility** for OpenClaw skill inventory management. It scans SKILL.md files and generates manifest reports.

## What This Tool Does NOT Do

- ❌ Collect, transmit, or store any credentials or API keys
- ❌ Make network requests or connect to external servers
- ❌ Execute arbitrary user input or shell commands (git is called via `spawnSync` with strict argument arrays)
- ❌ Access system files outside of the configured skill directories
- ❌ Contain any actual credential values

## Credential Pattern Detection

This tool includes regex patterns that match the **format** of common credential types (e.g., `sk-...`, `ghp_...`, `hf_...`). These patterns are used to **detect and mask** credentials found in SKILL.md files — replacing them with `********[MASKED]********` placeholders.

**These patterns do NOT contain any actual credential values.** They match structural characteristics only (prefix, length, character set).

## Git Operations

Git commands are executed via Node.js `spawnSync` with argument arrays. No user-supplied strings are interpolated into shell commands. Only the following git subcommands are used: `init`, `remote`, `add`, `commit`, `push`, `status`, `branch`, `diff`, `symbolic-ref`.

## Dependency

This tool has **zero runtime dependencies**. It uses only Node.js built-in modules (`fs`, `path`, `os`, `readline`, `child_process`).

## Reporting

If you find a genuine security issue, please open a GitHub Issue.
