# Worker output cleaning patterns

Use these patterns to turn noisy local CLI output into short supervisor-facing summaries.

## Remove or down-weight

- tool banners
- MCP startup lines
- provider/model/session metadata
- repeated shell framing
- empty lines and duplicate lines

## Preserve

- explicit failure reasons
- repository/path problems
- read-only or sandbox constraints
- missing credential/login messages
- build/test/review outcomes
- concise final worker conclusion when present

## Summary target

Aim for a short excerpt that helps the supervisor decide:
- still running
- completed
- failed
- blocked by environment
- needs review
