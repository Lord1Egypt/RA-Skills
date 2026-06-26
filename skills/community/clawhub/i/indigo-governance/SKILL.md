---
name: indigo-governance
description: "Query Indigo Protocol governance data including protocol parameters, polls, ."
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---

# Governance & Params

Query Indigo Protocol governance data including protocol parameters, temperature checks, polls.

## MCP Tools

| Tool | Description |
|------|-------------|
| `get_protocol_params` | Get current Indigo Protocol parameters |
| `get_temperature_checks` | Get active governance temperature checks |
| `get_polls` | Get governance polls and voting data |

## Sub-Skills

- [Protocol Params](sub-skills/protocol-params.md) — Query protocol parameters
- [Polls](sub-skills/polls.md) — Temperature checks and governance polls

## References

- [MCP Tools Reference](references/mcp-tools.md) — Detailed tool parameters and return types
- [Governance Concepts](references/concepts.md) — Voting process, protocol parameters, 
