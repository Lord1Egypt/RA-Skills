## Description:

Generates Markdown Notion templates for workspaces, databases, dashboards, wikis, project management, and personal systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Notion-importable Markdown structures and step-by-step implementation guidance for workspaces, databases, dashboards, wikis, projects, and personal templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an unrelated local data utility that is not clearly disclosed by the skill description.

Mitigation: Prefer invoking scripts/notion.sh directly for template generation and review scripts/script.sh before using add, list, search, export, or related utility commands.

Risk: The unrelated utility can store and log user input under the skill's local data directory.

Mitigation: Avoid entering sensitive information into the utility commands and use a controlled NOTION_TEMPLATE_DIR if those commands are needed.

## Reference(s):

- [Notion Template on ClawHub](https://clawhub.ai/bytesagain-lab/skills/notion-template)
- [bytesagain-lab publisher profile](https://clawhub.ai/user/bytesagain-lab)
- [BytesAgain homepage](https://bytesagain.com)
- [Notion Template Prompt Tips](tips.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with Notion-ready tables, page structures, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Template content varies by command, use case, and team size.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
