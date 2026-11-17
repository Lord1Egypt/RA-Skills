## Description:

XAUUSD is an institutional desk-level automated trading OS for XAU/USD and XAG/USD with an event-driven, risk-first, multi-engine architecture that runs as a continuous analysis and execution pipeline inside OpenClaw's trader agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cfilipemt](https://clawhub.ai/user/cfilipemt)

### License/Terms of Use:

MIT

## Use Case:

External users and trading agents use this skill to analyze XAU/USD and XAG/USD, generate trade plans, run advisory or automated execution workflows, monitor risk, and track performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated dashboard clients may expose trading state or change the system into live automated execution.

Mitigation: Bind the WebSocket to localhost or require authentication, keep port 3078 unexposed, and require explicit local approval for mode changes.

Risk: Automated execution and risk controls may be unreliable before validation with broker events.

Mitigation: Run only in Mode 1 or an isolated demo environment until short-order execution is fixed and all risk controls are tested against live or sandbox broker events.

Risk: Broker and API credentials can permit account access or message dispatch.

Mitigation: Use least-privilege credentials, keep secrets out of committed files, and avoid Mode 2 or Mode 3 with real funds until the security guidance is resolved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cfilipemt/skills/metals-desk-os)
- [MetaAPI](https://metaapi.cloud)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, trade plans, alerts, and status data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces trading analysis, execution guidance, operational modes, risk status, dashboard events, and alert payloads for an OpenClaw trading agent.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
