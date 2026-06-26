# Repository Analysis - googleworkspace/cli

## Scope of Investigation

Repository analyzed: `https://github.com/googleworkspace/cli`.
Observed latest commit during analysis:
- `d3e90e4931b28efb65814cc94be6a8c55baa4425`
- date: 2026-03-05
- summary: config path normalization to `~/.config/gws`

## Core Technical Findings

- Project is a Rust CLI (`gws`) with dynamic command generation.
- Command surface is built at runtime from Google Discovery docs, not static generated SDK crates.
- Two-phase parsing model:
  1. parse service and global flags
  2. fetch discovery and rebuild command tree
- Global output formats: `json`, `table`, `yaml`, `csv`.
- Pagination controls: `--page-all`, `--page-limit`, `--page-delay`.

## Authentication Findings

- `gws auth` supports `setup`, `login`, `status`, `export`, `logout`, `list`, `default`.
- Multi-account model with `--account` and account registry.
- Credentials are encrypted with AES-256-GCM and keyring/file fallback.
- Auth precedence:
  1. explicit access-token override
  2. explicit credentials-file override
  3. per-account encrypted credentials

## Security and Reliability Findings

- Input validation includes path safety and URL encoding helpers.
- Discovery responses are cached for 24 hours in `~/.config/gws/cache/`.
- Model Armor integration supported through `--sanitize` and sanitize mode env vars.
- Structured JSON errors include actionable fields like API enablement links.

## Agent Integration Findings

- `gws mcp` exposes API methods as MCP tools over stdio.
- Service list can be constrained (`-s drive,gmail`) or expanded (`-s all`).
- Workflows can be exposed via `-w` though some workflow MCP calls are still partial.
- Repository includes generated skills index and helper skills for common tasks.

## Practical Implication for This Skill

This skill should prioritize schema-first command construction, explicit auth/account routing, and strict change control for mutating commands.
