## Description:

What the desk does when something goes wrong on Hyperliquid - unknown send results, unexpected fills or positions, unprotected positions, stuck or orphaned orders, API outages, rate limiting, and suspected API wallet compromise. Contain first, reconcile from the exchange record, act only through approved tickets, then review. Use the moment anything does not match the ticket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Trading desk operators and supporting agents use this skill to contain and reconcile Hyperliquid order, position, connectivity, and API wallet incidents, route any response through approved tickets, and document the review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete because some local references could not be resolved, and it flags an external exchange URL for review.

Mitigation: Check that the referenced local playbooks are available and that the Hyperliquid endpoint is appropriate for your setup before installing.

Risk: Incident response actions can affect live orders and positions.

Mitigation: Reconcile against current exchange state and act only through an approved ticket or documented standing authority.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/hypergrok-desk-incident-response)
- [Hyperliquid Info API](https://api.hyperliquid.xyz/info)

## Skill Output:

**Output Type(s):** [Guidance, Text, API Calls]

**Output Format:** [Markdown incident response playbooks and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Procedural guidance for incident declaration, reconciliation, containment, escalation, and review.]

## Skill Version(s):

1.9.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
