## Description:

JPVerify: Japan business data for AI agents — verify Japanese companies (法人番号), qualified-invoice T-numbers (インボイス), invoice issuers (including registration on the invoice date) and suppliers; normalize and validate Japanese addresses; find a Japanese company from its English name; plus JP PINT e-invoice validation. Use when a task involves Japanese business documents or data and you need to pick the right check. Paid per call (API key credits or x402); a free guide tool is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[japanverify](https://clawhub.ai/user/japanverify)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents assisting developers, finance teams, or procurement staff use JPVerify to choose checks for Japanese company identities, invoice issuers, suppliers, addresses, and JP PINT invoices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice-upload examples may send complete invoice documents to JPVerify without a clear privacy warning.

Mitigation: Before using an upload flow, review what invoice data would leave the environment and confirm that transfer is allowed by your data-sharing rules.

Risk: The security assessment reports incomplete coverage for filings and regulated-business checks, so evidence for those capabilities is incomplete.

Mitigation: Review the filings and regulated-entity checks and decide whether their coverage is sufficient for the task before relying on them.

## Reference(s):

- [JPVerify API endpoints](references/endpoints.md)
- [JPVerify API examples](references/examples.md)
- [JPVerify API key documentation](https://api.jpverify.com/docs/api-key)
- [JPVerify x402 documentation](https://api.jpverify.com/docs/x402)
- [JPVerify website](https://www.jpverify.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Structured API requests and JSON responses, with shell commands and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid calls can incur per-call charges; batch operations are available for supported checks.]

## Skill Version(s):

1.3.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
