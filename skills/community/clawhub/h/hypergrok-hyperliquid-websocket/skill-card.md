## Description:

Subscribe to live Hyperliquid data over WebSocket from the desk computer - mids, order book, trades, candles, best bid/offer, and per-account fills, order updates and events - with raw JSON, Python SDK and TypeScript examples, plus how to run a supervised watch that logs to a file and alerts. Read-only. Use for monitoring, fill notifications and any watch that polling would make expensive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading desk operators use this skill to monitor Hyperliquid market data and account events through live WebSocket subscriptions. It provides read-only examples for notifications and supervised watches, including recovery guidance for reconnects and data gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supervised watch can run in the background and write logs continuously.

Mitigation: Confirm the background watch is expected, review its log location, and stop it when monitoring is no longer needed.

Risk: Some reference checks were incomplete, leaving two references unresolved by the scan.

Mitigation: Check the relevant protocol and SDK documentation before relying on behavior that depends on those references.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/hypergrok-hyperliquid-websocket)
- [Publisher profile](https://clawhub.ai/user/galleonlabs)
- [Repository cited in ATTRIBUTION.md](https://github.com/galleonlabs/hypergrok-trading-desk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON WebSocket examples, Python and TypeScript snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only monitoring examples.]

## Skill Version(s):

1.9.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
