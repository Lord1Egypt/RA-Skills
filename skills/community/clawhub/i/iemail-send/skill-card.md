## Description:

Send transactional email via Iemail OpenAPI. Configure via OpenClaw skill env only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-atlas](https://clawhub.ai/user/jack-atlas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send single transactional emails through the Dmartech/Iemail OpenAPI from an OpenClaw workspace configured with sender and API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send email content through an external Dmartech/Iemail API.

Mitigation: Use only approved sender accounts and do not send sensitive, regulated, or unauthorized content through the API.

Risk: The skill asks agents to read OpenClaw or workspace configuration files for credentials.

Mitigation: Provide only the required Iemail variables in an isolated environment and avoid allowing access to unrelated configuration or secrets.

Risk: The Python script can install missing dependencies at runtime without pinned versions.

Mitigation: Preinstall or pin required dependencies in the runtime environment before enabling the skill.

## Reference(s):

- [Dmartech Application](https://app.dmartech.cn/)
- [Iemail API Endpoint](https://iemail-api.dmartech.cn)
- [ClawHub Skill Page](https://clawhub.ai/jack-atlas/skills/iemail-send)
- [Publisher Profile](https://clawhub.ai/user/jack-atlas)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses from the email script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Iemail credential environment variables; sends content to an external email API.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
