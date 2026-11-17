## Description:

ISP API Tester helps agents automate Baiwang ISP open-platform API testing by preparing authenticated requests, running test cases, and generating reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squidtestgary](https://clawhub.ai/user/squidtestgary)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to create reusable API test configurations, exercise Baiwang ISP v6.0 and v7.0 interfaces in a controlled test environment, and review generated result reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API credentials, database data, access tokens, and generated reports that may contain sensitive information.

Mitigation: Rotate exposed credentials before use, install only in a controlled test environment, and treat generated reports as sensitive artifacts that require redaction before sharing.

Risk: API test configurations may target non-HTTPS URLs, increasing exposure of credentials or test data in transit.

Mitigation: Require HTTPS in environment-specific configuration before executing tests.

Risk: Database fixtures and configurable SQL can access live or sensitive data.

Mitigation: Use least-privilege read-only database accounts and review each config file's SQL and target URL before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/squidtestgary/skills/isp-api-tester)
- [Publisher profile](https://clawhub.ai/user/squidtestgary)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands; execution can produce HTML, JSON, and JavaScript report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports can contain request, response, token, and database-derived data and should be handled as sensitive artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
