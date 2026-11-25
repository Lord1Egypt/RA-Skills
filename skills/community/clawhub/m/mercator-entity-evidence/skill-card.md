## Description:

Provides company facts such as legal name, headquarters, executives, and funding with attributed source URLs, verified excerpts, retrieval times, and source agreement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arzuo](https://clawhub.ai/user/arzuo)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators can request company fields for a domain or name and inspect the supporting sources, excerpts, and conflicts before relying on the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests to its configured API origin, and the security scan reports incomplete reference resolution.

Mitigation: Review the configured API origin and scan status before use; the validation preflight is free and can be used first.

Risk: Paid enrichment calls can spend USDC from the user's wallet.

Mitigation: Use a payment signer or pre-signed X-PAYMENT header only with an intentional spend limit; no payment is needed for validation preflight.

Risk: A cited excerpt shows what a source says, not whether the claim is true; sources can conflict or be unavailable.

Mitigation: Inspect the cited URLs and excerpts, and treat UNKNOWN fields or unresolved conflicts as inconclusive.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/arzuo/skills/mercator-entity-evidence)
- [MERCATOR Entity Evidence service](https://mercator-entity-evidence.fly.dev)

## Skill Output:

**Output Type(s):** [JSON, Company evidence]

**Output Format:** [Structured JSON with per-field values, source URLs, excerpts, retrieval times, confidence, and source agreement]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include UNKNOWN fields and conflicting source claims; a paid call costs $0.10 USDC on Base when at least one requested field is newly verified.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
