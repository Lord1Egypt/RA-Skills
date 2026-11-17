## Description:

Use for tasks that read or modify Notion pages, data sources, or blocks via the Notion API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffreymaomao](https://clawhub.ai/user/jeffreymaomao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to search, inspect, query, create, update, append to, trash, and restore Notion workspace content through the public Notion API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live changes to Notion workspace content, including page property updates, appended blocks, trash, and restore actions.

Mitigation: Read existing objects before mutation, inspect database schemas before property writes, and ask the user to choose a target when requests are underspecified.

Risk: A Notion integration token may grant access beyond the intended workspace content if shared too broadly or stored carelessly.

Mitigation: Prefer runtime-provided NOTION_KEY or a secret manager, avoid plaintext token fallback unless file permissions are locked down, and share the integration only with needed pages or databases.

## Reference(s):

- [Notion API documentation](https://developers.notion.com)
- [ClawHub skill page](https://clawhub.ai/jeffreymaomao/skills/notion-tools)
- [Setup](references/setup.md)
- [Examples](references/examples.md)
- [Property Patterns](references/property-patterns.md)
- [Blocks And Formatting Edge Cases](references/blocks.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Notion API request payloads and operational guidance for live workspace changes.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
