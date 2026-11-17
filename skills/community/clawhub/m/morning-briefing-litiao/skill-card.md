## Description:

Generates a personalized morning briefing from today's reminders, unfinished Notion tasks, and optional vault storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

People who use Apple Reminders and Notion tasks can ask an agent for a morning briefing or daily plan. The skill summarizes same-day reminders and undone Notion tasks into a concise report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read personal reminder and task data.

Mitigation: Use it only in contexts where the user has explicitly requested a briefing and understands which local sources will be queried.

Risk: The skill can use a local Notion API key to query a configured tasks database.

Mitigation: Use a minimally scoped Notion integration, keep the key in local credential storage, and avoid exposing credentials in prompts or generated output.

Risk: Broad activation wording could cause the briefing workflow to run when the user expected only planning advice.

Mitigation: Require clear user confirmation before reading reminders, querying Notion, or writing briefing content.

Risk: Briefing content may be written to a vault if that workflow is enabled.

Mitigation: Confirm the destination and content before writing notes that include personal schedule or task information.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Usage Guide](artifact/references/USAGE.md)
- [ClawHub Skill Page](https://clawhub.ai/litiao1224/skills/morning-briefing-litiao)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown-style morning briefing with reminder and task sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on local reminder access, a configured Notion database ID, a local Notion API key, and any vault-writing workflow configured by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
