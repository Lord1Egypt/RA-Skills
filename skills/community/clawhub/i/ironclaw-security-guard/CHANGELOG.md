# Changelog

## Unreleased

- Prepared the plugin for community publishing with a user-owned npm package name, manifest versioning, and bundled `skills/` directory support.
- Fixed stateful regex reuse in scanning and redaction paths so repeated scans do not silently miss secrets or prompt-injection patterns.
- Added a lightweight `node:test` regression suite for shell blocking, prompt-injection detection, secret redaction, allowlist checks, and manual tool execution.
- Added a copy-pasteable OpenClaw plugin config example and README verification commands.

## 2026-03-24

- Added public skill metadata and OpenAI/Codex-facing skill card metadata.
- Added English and Chinese README documentation.
- Added contribution, security, and example documentation.
- Repositioned the repo as a public OpenClaw security plugin rather than just a code drop.
