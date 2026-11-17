# Changelog

## 2.2.0 — 2026-10-12

- Add bounded REST readers for profiles, action schemas, availability, history,
  calendar events and weather forecasts. REST needs no third-party dependency.
- Add optional one-shot WebSocket readers for entity/device/location registries,
  Assist configuration, Energy/statistics, repairs and automation/script definitions.
- Add configuration validation, exact target expansion and target-specific action
  discovery without execution.
- Correct forecast response handling, Kelvin light fields, direct-script variables,
  automation conditions, calendar bounds and notification examples.
- Enforce trusted origins, TLS verification, redirect/proxy refusal, response
  limits, credential redaction, deadlines and no automatic retries in readers.
- Document native MCP and direct API choices, permissions, unsupported commands
  and the distinction between mock tests and frontend verification.
- Keep curl bearer headers out of process arguments using stdin; document token
  authority, household privacy and inspected template queries.
- Add 60 tests and a Windows/Linux CI matrix for Python and WebSocket compatibility.

OpenClaw's existing environment and curl/jq dependency gates remain in place.
Python 3.10+ readers can run standalone. Optional WebSocket reads require
`websockets>=15.0.1,<18`. No device-control command is added to either reader.
