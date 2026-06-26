# MCP And Orchestration - MiniMax

Use this file when MiniMax is part of a tool-using workflow rather than a plain generation call.

## Core Posture

MCP expands what the model can reach.
Treat every MCP server as a trust boundary, not as a convenience toggle.

## Default Policy

- prefer no MCP unless the workflow truly needs external tools
- prefer local or tightly scoped MCP servers over broad remote ones
- require explicit approval before enabling any remote MCP host
- keep model choice and tool choice separate in the design

## What To Clarify First

- which host will run the MCP server
- what data the server can read or modify
- whether tool actions are read-only or can trigger side effects
- whether the user wants model reasoning only, tool execution, or both

## Orchestration Rules

- keep the MiniMax prompt focused on decision-making, not on embedding huge raw tool payloads
- summarize tool results before the next model step when possible
- if the tool can act destructively, insert an approval checkpoint before execution
- log approved hosts and scopes in `mcp-notes.md`

## Failure Signs

- the server is technically reachable but the user never approved its scope
- the model gets noisy because raw tool output is larger than the task needs
- the workflow mixes local-only assumptions with remote MCP execution
- retries keep hitting the same tool error because the issue is authorization, not prompt quality
