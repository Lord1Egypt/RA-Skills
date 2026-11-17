## Description:

Work with Notion databases, pages, and APIs. Use when user needs to create, read, update, or delete Notion pages and databases; automate Notion workflows; sync data between Notion and other apps; or build integrations with Notion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to connect agents to Notion workspaces, query databases, create and update pages, and support workflows such as task tracking, content calendars, CRM records, and knowledge-base updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify Notion pages and databases through a Notion integration token.

Mitigation: Use a Notion token with access limited to the minimum pages and databases required, and test create or update operations on non-production content first.

Risk: A Notion integration token could expose workspace content if shared, logged, or stored insecurely.

Mitigation: Keep NOTION_TOKEN out of logs and shared files, rotate it if exposure is suspected, and follow the server security guidance for token handling.

Risk: Dependency behavior may change if notion-client is installed without a pinned version.

Mitigation: Pin notion-client in the consuming environment when reproducible behavior is required.

## Reference(s):

- [Notion Integration Examples](references/examples.md)
- [Notion integrations setup](https://www.notion.so/my-integrations)
- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/notion-helper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit JSON-formatted Notion API responses when the bundled CLI is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
