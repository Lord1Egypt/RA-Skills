## Description:

Full Notion API skill — query databases, manage pages, append blocks, and search your entire workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fr3kstyle](https://clawhub.ai/user/fr3kstyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to automate Notion databases, pages, blocks, and workspace search from an agent-accessible command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Notion integration token and can read or modify shared Notion pages and databases.

Mitigation: Scope the Notion integration to only the pages and databases needed before use.

Risk: Create, update, append, and archive commands make real changes to a Notion workspace.

Mitigation: Review command arguments and target page or database IDs before executing write or archive actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fr3kstyle/skills/notion-workspace)
- [Notion API Endpoint](https://api.notion.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Notion integration token in NOTION_API_KEY and optionally a default database ID in NOTION_DATABASE_ID.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
