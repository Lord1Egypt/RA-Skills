## Description:

Place, manage, and cancel orders using REST API or SDK hooks. Covers market, limit, IOC, FOK, POST_ONLY order types and batch operations

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarnadas](https://clawhub.ai/user/tarnadas)

### License/Terms of Use:


## Use Case:

Developers building Orderly Network trading interfaces or automation use this skill to implement order placement, editing, cancellation, batch workflows, validation, and order monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers live trading actions, including order placement, editing, cancellation, batch cancellation, and cancel-all operations.

Mitigation: Use testnet or low-permission keys where possible and require human confirmation before placing, editing, canceling, batch-canceling, or canceling all orders.

Risk: Broad cancel-all workflows can affect more orders than intended.

Mitigation: Prefer scoped cancellations by symbol or specific order identifiers and avoid unscoped cancel-all operations.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/tarnadas/skills/orderly-trading-orders)
- [Orderly order API endpoint](https://api.orderly.org/v1/order)
- [Orderly symbol rules endpoint](https://api.orderly.org/v1/public/info/PERP_ETH_USDC)
- [Orderly batch order API endpoint](https://api.orderly.org/v1/batch-order)

## Skill Output:

**Output Type(s):** [Guidance, Code, API calls, Configuration]

**Output Format:** [Markdown with TypeScript examples and REST endpoint snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes order parameter guidance, validation checks, lifecycle operations, and rate-limit notes.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
