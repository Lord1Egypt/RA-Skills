## Description:

Checks Japanese suppliers and counterparties before payment using corporate-number, qualified-invoice, and address evidence, with FSA licence and EDINET checks where relevant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[japanverify](https://clawhub.ai/user/japanverify)

### License/Terms of Use:

MIT

## Use Case:

Procurement, accounts payable, and compliance teams use this skill when onboarding a Japanese supplier, reviewing an invoice, or deciding whether a counterparty needs manual review. It summarizes public registry evidence to inform a human decision.

### Deployment Geography for Use:

Japan

## Known Risks and Mitigations:

Risk: Supplier identifiers are sent to the external JPVerify service.

Mitigation: Submit only necessary identifiers that the user is entitled to process, and avoid unnecessary personal details.

Risk: Registry coverage gaps or ambiguous matches can leave a supplier check incomplete.

Mitigation: Review the returned evidence and coverage notes; leave approval decisions to a human and do not treat the result as a legal or KYB determination.

Risk: JPVerify calls are paid and batch checks can add up.

Mitigation: State the call count and total price and get approval before batch work or plans costing more than $0.50.

## Reference(s):

- [Endpoint guide](references/endpoints.md)
- [Request examples](references/examples.md)
- [JPVerify API key documentation](https://api.jpverify.com/docs/api-key)
- [JPVerify x402 documentation](https://api.jpverify.com/docs/x402)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Markdown evidence summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Organized by counterparty with evidence, source dates, coverage notes, and possible next steps.]

## Skill Version(s):

1.3.5 (source: server-resolved release metadata, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
