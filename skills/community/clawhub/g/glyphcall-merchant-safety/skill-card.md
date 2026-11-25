## Description:

Decide whether a shop, seller or destination domain is safe to transact with by combining a merchant trust verdict with a link-level phishing and redirect check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nutshell2000](https://clawhub.ai/user/nutshell2000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to vet a merchant domain or checkout link before paying. It requests a merchant trust or link safety verdict and presents the evidence returned so the agent can make an informed decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents running agentcash@latest, a mutable package version that may change between uses.

Mitigation: Review the package and pin a specific version before use; consider whether you trust agentcash and its external service.

## Reference(s):

- [Merchant Safety on ClawHub](https://clawhub.ai/nutshell2000/skills/glyphcall-merchant-safety)
- [Glyphcall Merchant Trust API](https://api.glyphcall.com/merchant/trust?name=<domain>)
- [Glyphcall URL Safety API](https://api.glyphcall.com/pack/url-safety?url=<url>)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Guidance]

**Output Format:** [Text summarizing merchant or link safety verdicts and the evidence returned by the service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report only the fields received; a missing signal is not a clean verdict, and the result is guidance rather than a guarantee against fraud or loss.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
