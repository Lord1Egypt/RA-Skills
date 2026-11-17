## Description:

Checks whether an entity publishes a specified blockchain contract address for a given chain and purpose, returning supporting sources and a transaction recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arzuo](https://clawhub.ai/user/arzuo)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and people preparing blockchain transactions use this skill to check whether the target entity published a specific chain, contract address, and purpose before transacting. It verifies address provenance, not contract safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contract lookup requests are sent to a remote service.

Mitigation: Review the domain, chain, address, and service destination before sending a request.

Risk: The paid route charges $0.25 USDC via x402; even a no-evidence result may still be charged.

Mitigation: Use the free preflight first, confirm the payment requirements, and approve the charge before calling the paid route.

Risk: A PASS result can be mistaken for a contract safety assessment.

Mitigation: Treat PASS only as evidence of the published target; assess audits and financial risks separately.

Risk: Changing the service URL when sending a payment header can direct the paid request to an unintended host.

Mitigation: Keep MERCATOR_BASE_URL pointed at the intended Mercator host when using X_PAYMENT.

## Reference(s):

- [MERCATOR service homepage](https://mercator-entity-evidence.fly.dev)
- [ClawHub skill release](https://clawhub.ai/arzuo/skills/mercator-address-evidence)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown guidance and example JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results describe the evidence sources and whether the candidate address is supported for the stated purpose.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
