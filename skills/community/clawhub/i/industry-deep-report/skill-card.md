## Description:

When a user specifies an industry segment or company, this skill performs deep research analysis and produces a structured report covering overview, competitors, trends, opportunities, risks, and intelligence insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neo-yu3](https://clawhub.ai/user/neo-yu3)

### License/Terms of Use:

MIT-0

## Use Case:

External users can request a paid deep report on a target industry segment or company. The agent coordinates payment, then returns a structured analysis covering market context, competitive landscape, trends, opportunities, risks, and actionable intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says this paid report skill handles user queries and payment credentials through unsafe, under-scoped mechanisms.

Mitigation: Review carefully before installation and avoid confidential business questions or payment-sensitive workflows until credential handling is hardened.

Risk: The security guidance identifies use of HTTP on a non-verifiable domain as a concern.

Mitigation: Use only after the service uses HTTPS on a verifiable domain and validates order numbers.

Risk: The security guidance says remote report structure should be treated as untrusted data.

Mitigation: Review returned report structure and generated reports before relying on them for business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neo-yu3/skills/industry-deep-report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report text with shell command workflow outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires successful payment before report generation.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
