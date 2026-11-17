## Description:

Submits HTTP status code and website accessibility requests to XiaoMeng AGI's paid analysis API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaomeng-agi](https://clawhub.ai/user/xiaomeng-agi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to create paid XiaoMeng AGI orders for HTTP status or website accessibility analysis and retrieve the results after payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user text, order data, and credentials to a paid third-party analysis API.

Mitigation: Do not submit internal URLs, secrets, proprietary prompts, or reusable credentials unless XiaoMeng AGI use and payment handling are approved.

Risk: The release is framed as an HTTP status checker but its behavior is a general paid analysis connector.

Mitigation: Review the submitted request and expected output before payment, and treat returned analysis as third-party guidance requiring validation.

## Reference(s):

- [API Reference](references/api-reference.md)
- [XiaoMeng AGI service homepage](https://xiaomeng-api.qisir.com)
- [ClawHub skill page](https://clawhub.ai/xiaomeng-agi/skills/http-status-code-check)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; sends request text, order numbers, and credentials to a paid third-party API.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter and README mention 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
