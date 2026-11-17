## Description:

Assist users in recording personal health data, including diet, weight, body fat, body measurements, exercise, sleep, and menstrual cycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[734818028](https://clawhub.ai/user/734818028)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to log personal Keep health records from natural language and optional images, including meals, workouts, weight, body measurements, sleep, and menstrual cycle entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health records and selected images may be sent to Keep's MCP service.

Mitigation: Use only with informed user consent, and confirm before saving sensitive records or uploading images.

Risk: Keep bearer tokens are stored locally under ~/.keepai/.env.

Mitigation: Restrict local file permissions, avoid exposing tokens in command history or logs, and revoke or clear credentials when access is no longer needed.

Risk: Broad health-logging triggers may activate the skill for personal data the user did not intend to save.

Mitigation: Review activation behavior and add a confirmation step for ambiguous or highly sensitive health entries.

Risk: Image upload behavior uses presigned upload URLs and fallback local file lookup.

Mitigation: Require trusted HTTPS upload hosts, avoid broad temporary-directory fallbacks, and upload only files the user explicitly selected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/734818028/skills/keep-record)
- [Keep MCP gateway](https://mcp.gotokeep.com/skills-mcp-gateway-page/v1)
- [Authentication reference](references/auth.md)
- [Health record reference](references/record.md)
- [Image upload reference](references/get-upload-url.md)
- [Revoke authentication reference](references/revoke-auth.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown responses with inline shell commands and JSON arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload selected images and send health-record text to Keep's MCP service after authentication.]

## Skill Version(s):

1.5.8 (source: server release metadata, skill metadata, _meta.json, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
