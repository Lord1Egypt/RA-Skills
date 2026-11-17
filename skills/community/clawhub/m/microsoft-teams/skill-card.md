## Description:

Helps agents access Microsoft Teams through Maton to manage teams, channels, messages, and meetings using an authorized connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Teams users and developers can ask an agent to list teams and channels, send messages, manage meetings, and access recordings or transcripts through their authorized Microsoft Teams connection. The skill also documents optional Maton functions and triggers for approved automations; Microsoft Teams is not itself a trigger event source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorizing a connection may expose Microsoft Teams data beyond the intended task.

Mitigation: Authorize Maton only when needed and keep OAuth scopes narrow.

Risk: Messages, meeting changes, deletions, functions, triggers, or destinations may cause unintended effects or disclose data.

Mitigation: Confirm each action and its target with the user before proceeding.

Risk: Using a raw API key can expose a long-lived credential.

Mitigation: Prefer OAuth through the CLI; avoid raw API keys unless the CLI cannot be used.

## Reference(s):

- [Microsoft Teams skill on ClawHub](https://clawhub.ai/byungkyu/skills/microsoft-teams)
- [Maton](https://maton.ai)
- [Microsoft Teams API overview](https://learn.microsoft.com/en-us/graph/api/resources/teams-api-overview)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions]

**Output Format:** [Markdown with command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions require an authorized Microsoft Teams connection; confirm writes with the user.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
