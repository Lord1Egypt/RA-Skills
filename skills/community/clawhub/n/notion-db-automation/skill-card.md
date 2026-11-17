## Description:

Automate common Notion database operations like batch page creation, data filtering, content generation, and export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[potatosolo](https://clawhub.ai/user/potatosolo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to automate repetitive Notion database work, including querying, bulk page creation, updates, exports, and workflow synchronization with other tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, archive, and export Notion workspace data.

Mitigation: Use a least-privilege Notion integration shared only with required databases and require explicit review before bulk update or archive workflows.

Risk: API tokens may be exposed if passed directly in code or command history.

Mitigation: Prefer OpenClaw secrets or environment injection instead of hardcoded tokens or command-line token arguments.

Risk: Exported CSV files can contain sensitive workspace data or active spreadsheet content.

Mitigation: Export only to controlled paths, treat CSV outputs as sensitive, and review them before sharing or opening in spreadsheet software.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/potatosolo/skills/notion-db-automation)
- [Notion integrations](https://www.notion.so/my-integrations)
- [Notion API](https://api.notion.com/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python examples and command-line usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify Notion database records and exported CSV files when the included scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
