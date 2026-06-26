# Policy

- active production-candidate validation chain: Base
- reviewed historical empty-scope chain: BSC
- authority mode: external signature, eoa-first
- write path: registry -> plan -> external signature -> MCP execute -> reconcile
- allowMainnetExecution default: false
- unknown, paused, or disabled markets must be rejected before execution
