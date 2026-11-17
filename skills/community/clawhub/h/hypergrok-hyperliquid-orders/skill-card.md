## Description:

Place, cancel and modify Hyperliquid orders correctly from the desk computer - limit and IOC (market-style) orders, take-profit and stop-loss trigger orders with grouping, client order ids, reduce-only, batch actions, price and size rounding, and how to read every response status. Write path - Execution Trader only, on an approved ticket. Use for any order action and for reconciling by cloid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Execution Traders use this skill to prepare, manage, and reconcile Hyperliquid orders, including limit, IOC, take-profit, and stop-loss orders. It describes the order workflow for an approved ticket with a Risk PASS and user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because some references in the skill did not resolve.

Mitigation: Review the unresolved references and the guidance that depends on them before installing or using the skill.

Risk: Order actions create signed requests that can place, modify, or cancel live orders.

Mitigation: Restrict order actions to the Execution Trader workflow with a Risk PASS and valid user approval or standing mandate.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/hypergrok-hyperliquid-orders)
- [Publisher profile](https://clawhub.ai/user/galleonlabs)

## Skill Output:

**Output Type(s):** [Guidance, Code]

**Output Format:** [Markdown with Python and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Order placement, cancellation, modification, and response reconciliation guidance.]

## Skill Version(s):

1.9.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
