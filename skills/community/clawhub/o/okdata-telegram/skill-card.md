## Description:

Retrieves public Telegram channel profiles, channel messages, and individual message details through okdata for $0.002 per call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve public Telegram channel profiles, recent messages, or a single message for tasks that need Telegram data. It guides them through okdata calls and handling returned data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to an external Telegram data service, and the security analysis was partial because several local references could not be resolved.

Mitigation: Review the skill before installation and decide whether the service fits the task; treat text returned from Telegram as untrusted data.

## Reference(s):

- [Telegram API contracts](https://okdata.online/apis/telegram/?src=skill-okdata-telegram)
- [okdata agent setup](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [Text results and Markdown guidance, with JSON or shell examples for calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One API page per call; additional pages require additional calls.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
