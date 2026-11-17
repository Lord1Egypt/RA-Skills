## Description:

Normalize, parse, validate, and geocode Japanese addresses, or look up Japanese postal codes, with JPVerify's evidence-backed matches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[japanverify](https://clawhub.ai/user/japanverify)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams can standardize Japanese addresses, check whether an address matches a required level, find coordinates, split address components, or look up postal-code areas. Calls use JPVerify's paid API, so choose the suitable endpoint and spend level for the task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Address information is sent to JPVerify's external API, and the security review was partial.

Mitigation: Send only the address fields needed, omit names and contact details, and confirm the API destination is trusted for your data.

Risk: Paid API calls and batch jobs can consume credits or an x402 payment budget.

Mitigation: Choose the cheapest suitable endpoint, check the credit balance, and confirm the total cost before a batch run.

## Reference(s):

- [JPVerify](https://www.jpverify.com)
- [JPVerify API key guide](https://api.jpverify.com/docs/api-key)
- [JPVerify x402 guide](https://api.jpverify.com/docs/x402)
- [Endpoint reference](artifact/references/endpoints.md)
- [Request examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON results with concise English or Japanese explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include match evidence and confidence where available; API calls are paid per successful request.]

## Skill Version(s):

1.3.5 (source: evidence.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
