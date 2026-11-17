## Description:

Build a non-custodial, unsigned Base token swap using the public Jarvis best-execution router when the buyer wants an opt-in live comparison between the existing 0x and OKX routes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yl124915300-dot](https://clawhub.ai/user/yl124915300-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and host agents use this skill when a buyer explicitly requests an exact-input Base swap and wants an optional Jarvis route comparison before sending unsigned transaction data through a host wallet flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external Jarvis router receives wallet and swap details and returns unsigned transaction calldata.

Mitigation: Use only when that data sharing is acceptable, and require the host wallet to decode and confirm token sold, token received, amount, recipient, fees, spender, and contract target before approval.

Risk: Route responses and calldata are externally generated and only partially validated locally.

Mitigation: Treat every quote and unsigned transaction as untrusted; rely on the adapter's Base-only checks and require independent buyer or wallet approval before any broadcast.

## Reference(s):

- [Jarvis Router homepage](https://jarvis-orderflow-router.yl124915300.workers.dev/)
- [Jarvis Router route endpoint](https://jarvis-orderflow-router.yl124915300.workers.dev/v1/route)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON responses with route status, fee disclosure, buyer approval requirement, and unsigned send_calls input when a route is available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Base only; supports USDC, WETH, and DAI; buyer approval required; no signing, broadcasting, custody, or gas payment.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
