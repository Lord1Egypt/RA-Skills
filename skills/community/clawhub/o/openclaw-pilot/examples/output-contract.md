# Example: output contract

## Required delivery contract

OpenClaw Pilot outputs exactly two assistant messages for planning/continuation replies.

### Message 1 — human-readable

May include sections such as:

- blueprint
- feedback contract
- next command
- rationale

Must not include the packet block.

### Message 2 — packet-only

Must contain only:

```text
[OPENCLAW_EXECUTION_PACKET v1]
...
[END_OPENCLAW_EXECUTION_PACKET]
```

Must not include:

- section headers like `A.`, `B.`, `C.`, `D.`
- explanatory prose
- continuation hints
- extra status text before or after the block

## Regression check

Both `/pilot <goal>` and `/pilot next <pilot_id> <feedback>` must honor the same contract.