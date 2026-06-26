---
description: Run nella MCP tools — search code, get context, manage assumptions and dependencies
argument-hint: [context|search|assumptions|deps|index] [args]
allowed-tools: [mcp__nella__nella_index, mcp__nella__nella_search, mcp__nella__nella_get_context, mcp__nella__nella_add_assumption, mcp__nella__nella_check_assumptions, mcp__nella__nella_check_dependencies, Read, Glob, Grep, Bash]
---

# /nella

The user invoked `/nella` with arguments: $ARGUMENTS

## Instructions

Use nella MCP tools based on the arguments:

- **no args** or **context**: Call `nella_get_context` to show session state, recent changes, and assumptions.
- **search `<query>`**: Call `nella_search` with the provided query to find relevant code.
- **assumptions**: Call `nella_check_assumptions` to review all tracked assumptions.
- **deps**: Call `nella_check_dependencies` to check for dependency changes.
- **index**: Call `nella_index` to index or re-index the workspace.

If no arguments are given, default to `nella_get_context`.

Summarize results clearly after running the tool(s).
