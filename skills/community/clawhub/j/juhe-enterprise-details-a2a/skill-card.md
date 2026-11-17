## Description:

Queries Juhe Data for detailed Chinese enterprise registration information by company name, registration number, or unified social credit code after an A2M/HTTP 402 payment flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to purchase and retrieve structured enterprise registration reports for business verification, counterparty checks, and review of shareholders, officers, branch records, changes, and abnormal operation records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install a mutable Alipay payment package at runtime for the wallet and payment workflow.

Mitigation: Review the payment dependency before installation, prefer a pinned and verified Alipay payment package version, and avoid running the install in an environment with unrelated credentials or sensitive files.

Risk: The workflow sends the queried company name, registration number, or unified social credit code to Juhe and routes payment details through the Alipay payment skill.

Mitigation: Confirm user consent before payment, send only the required keyword, and avoid storing or logging raw query text, complete payment responses, or order details.

Risk: Enterprise registry results can be delayed, incomplete, or unsuitable as the only basis for commercial decisions.

Mitigation: Present the report as reference information and verify material decisions against official registration sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-enterprise-details-a2a)
- [Publisher profile: juhemcp](https://clawhub.ai/user/juhemcp)
- [Skill README](artifact/README.md)
- [Output format](artifact/OUT_FORMAT.md)
- [Juhe A2A enterprise query endpoint](https://apis.juhe.cn/a2a/query)

## Skill Output:

**Output Type(s):** [Markdown, API calls, Shell commands, Guidance]

**Output Format:** [Markdown report with structured tables after a JSON API response; payment setup guidance may include shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires one keyword: enterprise full name, registration number, or unified social credit code.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
