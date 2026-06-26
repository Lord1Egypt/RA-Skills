# openclaw-skill-lingua-universale

> **Verify agent-to-agent communication against session type protocols.**
> Mathematical proofs, not trust.

An MCP (Model Context Protocol) server that exposes [Lingua Universale](https://github.com/rafapra3008/cervellaswarm) protocol verification as tools for Claude Code, Cursor, and OpenClaw-compatible AI agents.

## What is Lingua Universale?

Lingua Universale (LU) is a session type system for AI agent communication. It lets you define protocols formally and verify that every message follows the specification -- preventing the "$34K bug" class of failures where agents silently deviate from the agreed communication pattern.

## Quick start

```bash
# Run as MCP server (uvx, no install needed)
uvx openclaw-skill-lingua-universale

# Or install and run
pip install openclaw-skill-lingua-universale
lu-mcp
```

## Tools

| Tool | What it does |
|------|-------------|
| `lu_load_protocol` | Parse a `.lu` protocol definition, extract roles/steps/properties |
| `lu_verify_message` | Check if a message is valid in the context of a session |
| `lu_check_properties` | Verify formal safety properties (deadlock-free, terminates, etc.) |
| `lu_list_templates` | Browse 20 standard library protocols across 5 categories |

## Example

```python
# In Claude Code with this MCP server configured:

# Load a protocol
result = lu_load_protocol("""
protocol RequestResponse:
    roles: client, server

    client asks server to process request
    server returns response to client

    properties:
        always terminates
        no deadlock
""")

# Verify a message
check = lu_verify_message(
    protocol_text=<above>,
    messages=[{"sender": "client", "receiver": "server", "action": "ask"}],
    next_message={"sender": "server", "receiver": "client", "action": "return"}
)
# -> {"valid": true, "next_expected": "protocol complete"}

# Check formal properties
props = lu_check_properties(<protocol_text>)
# -> all_passed: true
# -> always terminates: PROVED
# -> no deadlock: PROVED

# Browse standard library
templates = lu_list_templates(category="ai_ml")
# -> rag_pipeline, agent_delegation, tool_calling, human_in_loop, consensus
```

## Standard library (20 protocols)

| Category | Protocols |
|----------|-----------|
| **Communication** (5) | request_response, ping_pong, pub_sub, scatter_gather, pipeline |
| **Data** (3) | crud_safe, data_sync, cache_invalidation |
| **Business** (4) | two_buyer, approval_workflow, auction, saga_order |
| **AI/ML** (5) | rag_pipeline, agent_delegation, tool_calling, human_in_loop, consensus |
| **Security** (3) | auth_handshake, mutual_tls, rate_limited_api |

All 20 protocols cover all 9 formal property kinds:
`always terminates`, `no deadlock`, `no deletion`, `ordering`,
`exclusion`, `role exclusive`, `confidence >=`, `trust >=`, `all roles participate`.

## Adding to Claude Code

```json
{
  "mcpServers": {
    "lingua-universale": {
      "command": "uvx",
      "args": ["openclaw-skill-lingua-universale"]
    }
  }
}
```

## Requirements

- Python >= 3.11
- `cervellaswarm-lingua-universale >= 0.3.3` (auto-installed)
- `mcp >= 1.0` (auto-installed)
- No API keys. No network calls during verification.

## License

Apache-2.0 -- see [LICENSE](../LICENSE) in the root repository.

## Academic foundation

Built on multiparty session types (Honda, Yoshida, Carbone -- POPL 2008)
and the Scribble session type toolchain (Imperial College London).

---

*Part of CervellaSwarm -- the AI agent swarm with a verified communication backbone.*
