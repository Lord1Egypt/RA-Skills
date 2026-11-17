## Description:

调用久吾消息网关 HTTP 接口向企业内部联系人发送通知、提醒或批量消息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[05u](https://clawhub.ai/user/05u)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and internal operations teams use this skill to send company message gateway notifications or reminders to one or more employee IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send employee IDs and message contents over plaintext HTTP when the default gateway URL is used.

Mitigation: Use an approved HTTPS gateway whenever available and avoid sensitive message contents unless the gateway is secured.

Risk: The script loads broader OpenClaw environment files while only needing the message gateway URL.

Mitigation: Review configuration access before installation and prefer limiting the script to JIUWU_MESSAGE_GATEWAY_URL.

Risk: The release security verdict is suspicious for normal deployment.

Mitigation: Install only in a trusted internal environment after reviewing the security guidance and intended gateway endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/05u/skills/jiuwu-message)

## Skill Output:

**Output Type(s):** [Shell commands, Code, API Calls, Configuration]

**Output Format:** [JSON response from a Python script or Python function call]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends employee IDs, message text, and an optional title to the configured message gateway.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
