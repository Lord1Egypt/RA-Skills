## Description:

Checks Japanese qualified invoice registration numbers, matches issuers with invoice and supplier details, and reports registration status for a specified date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[japanverify](https://clawhub.ai/user/japanverify)

### License/Terms of Use:

MIT-0

## Use Case:

Accounts payable teams and agents use this skill to check Japanese T-numbers, compare invoice issuer details with registry records, and match invoices against supplier master data.

### Deployment Geography for Use:

Japan

## Known Risks and Mitigations:

Risk: Invoice registration numbers and issuer details sent for checking may be processed by an external service.

Mitigation: Send only fields needed for the check and only data the user is authorized to share; do not send personal details that are unnecessary.

Risk: Successful API checks incur per-call charges and may consume prepaid credits or x402 funds.

Mitigation: Tell the user the total before batch checks, obtain approval for the planned spend, and stay within any approved budget.

## Reference(s):

- [JPVerify API documentation: API keys](https://api.jpverify.com/docs/api-key)
- [JPVerify API documentation: x402 payments](https://api.jpverify.com/docs/x402)
- [Endpoint reference](artifact/references/endpoints.md)
- [Request examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Text or JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes registration status, registered name, relevant dates, and registry data-as-of date.]

## Skill Version(s):

1.3.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
