## Description:

Helps agents check L2 network health before transactions and optionally request a behavioral passport for the caller.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kant19801201behax5](https://clawhub.ai/user/kant19801201behax5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check L2 network conditions before a transaction, swap, bridge, or x402 payment, and optionally request a passport describing the caller.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A free health verdict reflects network conditions about a minute earlier and cannot guarantee execution safety.

Mitigation: Treat the delayed verdict as a signal, not a guarantee; check near transaction time.

Risk: The live health endpoint can charge an x402-capable wallet.

Mitigation: Use the free delayed endpoint for normal timing; use the live endpoint only when the wallet and charge are intended.

Risk: The passport request sends caller request metadata to a third-party service for classification.

Mitigation: Use the passport only when sharing caller metadata with that service is acceptable.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/kant19801201behax5/skills/phoenix-execution-check)
- [Phoenix Zero endpoint documentation](https://rtt.phoenix-ai.work/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown guidance with curl commands and JSON response interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free delayed health checks, optional paid live checks, and a caller-only passport.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
