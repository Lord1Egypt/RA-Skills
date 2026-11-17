## Description:

Helps agents work with Notion pages and databases through the official Notion API, including CRUD workflows and Markdown conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to automate Notion workspaces by creating, querying, updating, and deleting pages or databases and converting Markdown into Notion block JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mutate Notion workspace content through create, update, and delete actions.

Mitigation: Use a least-privilege Notion integration shared only with required pages or databases, and explicitly confirm mutation actions before execution.

Risk: The skill requests broad local command and file authority that is not clearly bounded to Notion tasks.

Mitigation: Run it in a constrained agent environment and review proposed shell commands and local file operations before allowing execution.

Risk: A leaked Notion API token could expose or alter connected workspace data.

Mitigation: Keep the token in an environment variable, avoid committing it to files, and rotate it when access changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/notion-skill-2)
- [Notion Integration Setup](https://www.notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Notion API request and response JSON, Markdown-to-block conversion examples, and environment variable setup guidance.]

## Skill Version(s):

1.0.0 (source: release evidence; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
