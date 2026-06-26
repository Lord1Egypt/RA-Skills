---
name: lingua-universale
version: 0.1.0
description: Verify agent-to-agent communication against session type protocols. Mathematical proofs, not trust.
author: CervellaSwarm
homepage: https://github.com/rafapra3008/cervellaswarm
tags: [protocol-verification, session-types, mcp, ai-agents, formal-methods]
user-invocable: true
metadata:
  clawdbot:
    emoji: "🔬"
    requires:
      bins:
        - uvx
      env: []
---

# Lingua Universale - Protocol Verification Skill

## What it does

Verifies that agent-to-agent messages follow a formally defined protocol
using **session types** -- the same mathematical framework used in distributed
systems research (Honda/Yoshida POPL 2008, Scribble, MPST).

No API keys required. No external services. Runs entirely locally.

## When to use

- Before sending a message to another agent: confirm the message is expected
- After a conversation: validate the full transcript against the protocol
- During design: check safety properties (no deadlock, always terminates)
- When choosing a protocol pattern: browse 20 standard library templates

## Tools provided

### `lu_load_protocol`

Parse a `.lu` protocol definition and extract its structure.

Input: `protocol_text` (string) -- full content of a `.lu` file
Output: JSON with protocol name, roles, steps, choices, and declared properties

### `lu_verify_message`

Check if a message is valid in the context of an ongoing session.

Input:
- `protocol_text` (string) -- the protocol definition
- `messages` (list) -- already-sent messages: `[{"sender": "a", "receiver": "b", "action": "ask"}]`
- `next_message` (dict) -- message to validate: `{"sender": "b", "receiver": "a", "action": "return"}`

Output: `{"valid": true, "next_expected": "..."}` or `{"valid": false, "violation": "...", "expected": "...", "got": "..."}`

### `lu_check_properties`

Verify the formal safety properties declared in a protocol.

Input: `protocol_text` (string)
Output: JSON with per-property verdicts (PROVED / SATISFIED / VIOLATED / SKIPPED) and evidence

Supported properties:
- `always terminates` -- no infinite loops
- `no deadlock` -- no role waits forever
- `no deletion` -- no destructive operations
- `X before Y` -- message ordering constraint
- `role cannot send message` -- exclusion
- `role exclusive message` -- only this role may send this message
- `confidence >= level` -- minimum confidence threshold
- `trust >= tier` -- minimum trust tier
- `all roles participate` -- every role sends at least one message

### `lu_list_templates`

Browse the 20 protocols in the Lingua Universale standard library.

Input: `category` (optional string) -- filter by: communication, data, business, ai_ml, security
Output: JSON with template names, categories, property highlights, and usage instructions

## Example workflow

```
# 1. Choose a protocol template
lu_list_templates(category="ai_ml")
# -> rag_pipeline, agent_delegation, tool_calling, human_in_loop, consensus

# 2. Load and inspect the protocol
lu_load_protocol("""
    protocol AgentDelegation:
        roles: supervisor, worker, validator
        supervisor asks worker to execute task
        worker returns result to supervisor
        supervisor asks validator to audit result
        validator returns verdict to supervisor
        properties:
            always terminates
            no deadlock
            all roles participate
            trust >= standard
""")

# 3. Verify messages as they flow
lu_verify_message(
    protocol_text=<above>,
    messages=[
        {"sender": "supervisor", "receiver": "worker", "action": "ask"}
    ],
    next_message={"sender": "worker", "receiver": "supervisor", "action": "return"}
)
# -> {"valid": true, "next_expected": "supervisor -> validator : audit_request"}

# 4. Check formal properties
lu_check_properties(<protocol_text>)
# -> all_passed: true, PROVED: always terminates, no deadlock, all roles participate
```

## Protocol syntax (.lu)

```
protocol Name:
    roles: role1, role2, role3

    role1 asks role2 to do something
    role2 returns result to role1

    when role1 decides:
        approve:
            role1 tells role3 about decision
        reject:
            role1 sends error to role3

    properties:
        always terminates
        no deadlock
        all roles participate
```

Valid actions: `asks`, `returns`, `sends`, `proposes`, `tells`

## Installation

```bash
# As a Claude Code MCP server
uvx openclaw-skill-lingua-universale

# Or install directly
pip install openclaw-skill-lingua-universale
lu-mcp  # starts stdio MCP server
```

## Academic references

- Honda, Yoshida, Carbone - "Multiparty Asynchronous Session Types" (POPL 2008)
- Scribble Project - session type toolchain (Imperial College London)
- Dezani-Ciancaglini et al. - "Session Types for Access and Information Flow Control" (2021)
