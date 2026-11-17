## Description:

How the desk watches markets and the account between trades using Grok Bot routines and WebSocket or polling watches, including desk briefs, book checks, funding and price watches, alert conditions, and what a watch may and may not do.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Traders and desk operators use the skill to prepare market and account briefs, monitor prices, funding, positions, and order events, and receive alerts when conditions change or data becomes unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A standing mandate may allow a proposal to proceed without per-action approval after Risk and mandate checks.

Mitigation: Review the mandate and the routine's approval boundary before enabling it; keep watches limited to alerts and proposals.

Risk: The security scan could not resolve three references, so its evidence is incomplete.

Mitigation: Review the unresolved references and their behavior before deployment.

## Reference(s):

- [HyperGrok Desk Monitoring release page](https://clawhub.ai/galleonlabs/skills/hypergrok-desk-monitoring)
- [Publisher profile: galleonlabs](https://clawhub.ai/user/galleonlabs)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files]

**Output Format:** [Markdown briefs, alerts, and tables, with saved monitoring records where configured]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Monitoring guidance is read-only: watches may fetch, compute, save, and alert, but do not place or change orders.]

## Skill Version(s):

1.9.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
