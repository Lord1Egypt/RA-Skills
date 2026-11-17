## Description:

亚马逊广告（Amazon Ads）报告一站式获取技能，覆盖 Sponsored Products (SP) / Sponsored Brands (SB) / Sponsored Display (SD) 报告类型，自动创建、等待、下载和解压报告并返回结构化数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon Ads operators, ecommerce analysts, and agent developers use this skill to retrieve SP, SB, and SD advertising performance reports with explicit report type, grouping, column, date range, and filter choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan notes redirectable credential-bearing endpoints and API key handling in the local environment.

Mitigation: Use a secret manager for LinkFox API keys, avoid endpoint override environment variables, and review configured endpoints before execution.

Risk: The security scan notes unauthenticated local report serving and possible exposure of report links or local file paths.

Mitigation: Disable local HTTP serving unless needed, keep report links and paths out of shared contexts, and rely on short-lived local access when a link is required.

Risk: The security scan notes silent feedback reporting plus onboarding and billing flows.

Mitigation: Require explicit approval before feedback submission, dependency installation, SMS or phone onboarding, or paid order creation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-ads-report)
- [Amazon Ads Reporting v3 Report Types](https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types)
- [API Parameters and Fields Reference](references/api.md)
- [Onboarding and Billing Reference](references/onboarding.md)
- [Report Types Index](references/report-types/index.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON parameters, shell commands, and report result JSON or summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes complete report responses to a local JSON file and may return a temporary local download URL for extracted report data.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
