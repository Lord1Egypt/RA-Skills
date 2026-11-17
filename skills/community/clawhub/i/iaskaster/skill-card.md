## Description:

iaskaster helps an agent collect Bazi birth details, authenticate to the external iaskmaster.cn service, and generate or retrieve fortune-analysis PDF reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjlzw](https://clawhub.ai/user/tjlzw)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to collect birth details, use verification-code login, submit an analysis request, and retrieve Bazi reports, report lists, account balance details, recharge links, and downloaded PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends phone or email login data and exact birth details to an external service.

Mitigation: Use the skill only with explicit user consent for that data sharing, and avoid submitting unnecessary personal details.

Risk: The report-reading tool can read arbitrary local files.

Mitigation: Constrain file access to generated report locations before deployment and review requested file paths before execution.

Risk: Tokens are stored or exposed with weak boundaries.

Mitigation: Protect token storage, avoid sharing command output that may include tokenized report links, and prefer a scoped token-handling design.

Risk: The API destination can be configured and is not proven allowlisted by the artifact evidence.

Mitigation: Allowlist the expected iaskmaster.cn endpoint and review any custom API URL before use.

Risk: The installer modifies OpenClaw configuration.

Mitigation: Review installer changes and back up configuration before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjlzw/skills/iaskaster)
- [Publisher profile](https://clawhub.ai/user/tjlzw)
- [iaskmaster external service](https://iaskmaster.cn)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Text and Markdown responses with shell-command examples; downloaded reports are PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires verification-code login and network access to the external iaskmaster.cn service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
