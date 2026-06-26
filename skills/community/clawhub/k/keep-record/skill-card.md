## Description: <br>
Assists users in recording personal health data, including diet, weight, body fat, body measurements, exercise, sleep, and menstrual cycle, when they clearly intend to record, log, check in, or save health-related information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[734818028](https://clawhub.ai/user/734818028) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to save personal health check-ins, including meals, drinks, weight, body measurements, workouts, sleep, and menstrual cycle notes, into Keep App. The skill supports natural-language records and optional image uploads through the Keep MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local account tokens are stored on the user's device. <br>
Mitigation: Install only on trusted devices, protect the local environment, and use the documented revoke or clear flow when local Keep access is no longer needed. <br>
Risk: The skill can upload user-provided images while saving health records. <br>
Mitigation: Provide only images intended for upload to Keep, and consider requiring confirmation before each save. <br>
Risk: Install-time behavior writes Keep configuration locally and can clear prior credentials when the MCP URL changes. <br>
Mitigation: Review the postinstall behavior before installation and expect users to reauthenticate after changing the configured Keep MCP endpoint. <br>
Risk: Broad activation may cause health-related statements to be routed to this skill automatically. <br>
Mitigation: Use explicit user confirmation for sensitive records or ambiguous logging requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/734818028/keep-record) <br>
- [Keep MCP service](https://mcp.gotokeep.com/skills-mcp-gateway-page/v1) <br>
- [Authentication workflow](references/auth.md) <br>
- [Health record tool](references/record.md) <br>
- [Image upload workflow](references/get-upload-url.md) <br>
- [Revoke authentication](references/revoke-auth.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce MCP tool calls for authentication, image upload, health-record creation, and logout flows.] <br>

## Skill Version(s): <br>
1.5.8 (source: evidence release metadata, package.json, _meta.json, and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
