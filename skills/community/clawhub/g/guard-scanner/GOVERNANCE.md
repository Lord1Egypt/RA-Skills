# Governance

## Project Scope

`guard-scanner` is an OSS security scanner focused on agent skills, MCP-connected workflows, and related runtime guardrails.

This repository governs:
- static detection patterns
- runtime tool-call guard logic
- MCP server and CLI behavior
- test corpus, quality gates, and release assets

## Decision Making

- The maintainer is responsible for final decisions on releases, threat model changes, and security-sensitive behavior.
- Behavior-changing pattern updates should land with tests, rationale, and a false-positive discussion.
- Security fixes take precedence over feature work.

## Change Policy

- Breaking changes should be documented in `CHANGELOG.md` and released in a new major version.
- New rules should include both malicious coverage and false-positive guard coverage.
- Claims in README / SKILL / plugin metadata must match `docs/spec/capabilities.json`.
