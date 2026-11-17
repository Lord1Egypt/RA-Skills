## Description:

Check and control iAqualink pool and spa systems, including temperatures, pumps, heaters, lights, chlorinators, schedules, and scenes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Pool owners and operators use the skill to check iAqualink system readings and manage compatible pool or spa equipment, chemistry controls, schedules, and scenes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pool and spa controls can change heating, chlorine output, or schedules.

Mitigation: Review the change preview and confirm it explicitly before execution.

Risk: The skill uses account credentials and a compatible external server.

Mitigation: Use a trusted iaqualink-mcp server and protect account credentials.

Risk: Some control paths are untested, and a change may be accepted without immediate verification.

Mitigation: Recheck system status before retrying an unconfirmed change, and do not blindly retry toggle commands.

## Reference(s):

- [ClawHub iaqualink skill page](https://clawhub.ai/chrischall/skills/iaqualink)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Text]

**Output Format:** [Structured tool results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include status readings, change previews, and confirmation results.]

## Skill Version(s):

0.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
