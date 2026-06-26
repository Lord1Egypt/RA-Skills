# Simulation - Google Workspace CLI

## Goal

Validate whether `google-workspace-cli` can compete for users searching operational Google Workspace command execution rather than generic productivity advice.

## Market Snapshot (from local dataset)

| Skill | Positioning | Downloads (snapshot) | Notes |
|-------|-------------|----------------------|-------|
| `gog` | generic Google Workspace CLI | 16k+ | very broad summary, weaker governance framing |
| `gogcli` | CLI variant | 2k+ | narrower and older positioning |
| `google-workspace-mcp` | no cloud console framing | 3k+ | strong ease-of-setup angle |
| `google-workspace-admin` | admin-centric | 6k+ | focused on admin SDK, less cross-service CLI coverage |

## Differentiation Hypothesis

`google-workspace-cli` should win when the user intent includes:
- command-level execution with schema introspection
- auth/account routing discipline
- MCP exposure with tool-budget control
- change control for high-impact operations

## Query Set

1. google workspace cli
2. gws cli
3. google workspace api cli
4. gmail drive calendar cli automation
5. google workspace mcp cli

## Variant Matrix

| Variant | Name | Description focus | Expected strength |
|---------|------|-------------------|------------------|
| A | Google Workspace CLI | dynamic discovery + auth safety | balanced ranking |
| B | GWS CLI for Google Workspace | shorter brand + command speed | stronger for `gws cli` |
| C | Google Workspace API CLI | API-first and schema-first framing | stronger for API-heavy queries |

## Recommended Direction

Ship Variant A because it balances discoverability (`google workspace cli`) with operational credibility (schema-first, auth-safe, change-controlled workflows).
