## Description:

Find and verify Japanese companies through registry lookups, identity matching, status checks, and company pre-check reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[japanverify](https://clawhub.ai/user/japanverify)

### License/Terms of Use:

MIT-0

## Use Case:

Teams checking Japanese vendors or counterparties can use the skill to identify a company, confirm its corporate number and status, and review registry-based company information. It helps resolve registered names and prepare a public-registry pre-check before onboarding or payment.

### Deployment Geography for Use:

Japan

## Known Risks and Mitigations:

Risk: Company identifiers and related fields are sent to JPVerify for paid API lookups.

Mitigation: Send only fields needed for the check that you are entitled to process, and confirm the external service is an acceptable destination.

Risk: Successful API calls can consume prepaid credits or require an x402 payment.

Mitigation: Review per-call prices and available credits before running checks; confirm the total cost before a batch or other large run.

## Reference(s):

- [Endpoint reference](references/endpoints.md)
- [Request examples](references/examples.md)
- [JPVerify](https://www.jpverify.com)
- [API key documentation](https://api.jpverify.com/docs/api-key)
- [x402 payment documentation](https://api.jpverify.com/docs/x402)
- [ClawHub release page](https://clawhub.ai/japanverify/skills/jp-company-verify)
- [Release notes](https://github.com/japanverify/jpverify-skills/releases/tag/v1.3.5)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured company lookup results with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include candidate matches and registry evidence; they are public-registry pre-checks, not full KYB, AML, or sanctions screening.]

## Skill Version(s):

1.3.5 (source: server-resolved release metadata; artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
