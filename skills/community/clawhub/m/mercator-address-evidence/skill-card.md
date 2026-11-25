## Description:

Checks whether an entity publishes a candidate contract address for a stated chain and purpose, and returns source evidence with a derived transact decision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arzuo](https://clawhub.ai/user/arzuo)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to check whether a candidate smart contract address matches an entity's published address for a specific chain and purpose before preparing a transaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send the submitted domain, chain, and address data to an external endpoint.

Mitigation: Review the request fields and use the service only when that disclosure is acceptable.

Risk: Coverage is partial, and some local references could not be resolved.

Mitigation: Use the free preflight to check current coverage before making a paid request.

Risk: The paid endpoint charges $0.25 USDC per verified call from the caller's wallet.

Mitigation: Use a bounded wallet or signer and run the free preflight before paying.

## Reference(s):

- [MERCATOR Address Evidence service and free preflight](https://mercator-entity-evidence.fly.dev)
- [ClawHub release page](https://clawhub.ai/arzuo/skills/mercator-address-evidence)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON evidence with a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source URLs and excerpts; the transact decision is derived from the evidence.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
