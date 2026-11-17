## Description:

Kim Msg Skill sends Kuaishou Kim instant messages through group webhooks or direct message-account APIs, with credential loading from environment variables or documented local credential files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegodamn](https://clawhub.ai/user/leegodamn)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to send Kim notifications, alerts, daily reports, and direct messages from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message text is sent to Kim service endpoints.

Mitigation: Avoid sending highly sensitive content unless the deployment and Kim workspace policies permit it.

Risk: Kim credentials are loaded from KIM_* environment variables or documented local credential files.

Mitigation: Use tightly scoped Kim credentials, restrict credential-file permissions, and keep those files out of shared workspaces and source control.

Risk: Tokens or secrets may appear in URL logs or local process arguments during sending.

Mitigation: Run the skill only in trusted environments, limit command logging, and rotate credentials if exposure is suspected.

## Reference(s):

- [Kim official website](https://kim.kuaishou.com/)
- [ClawHub skill page](https://clawhub.ai/leegodamn/skills/kim-msg)
- [Publisher profile](https://clawhub.ai/user/leegodamn)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API Calls, Markdown, Text]

**Output Format:** [Markdown or plain text message content sent through shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Kim webhook or app credentials supplied through environment variables or documented local credential files.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
