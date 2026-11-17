## Description:

Manage Notion workspaces by searching pages, reading content, creating database pages, appending blocks, and listing databases through the Notion REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrnsmh](https://clawhub.ai/user/mrnsmh)

### License/Terms of Use:

MIT

## Use Case:

Developers and workspace operators use this skill to manage Notion pages and databases from an agent workflow, CLI, or importable Python module. It supports search, page reads, database page creation, text appends, and database listing for Notion integrations with appropriate access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill ships and uses an embedded Notion token that could expose or modify a workspace the user did not intend to use.

Mitigation: Remove the embedded token, rotate or revoke the exposed Notion integration token, and require users to provide their own NOTION_TOKEN before installation or use.

Risk: Create and append commands perform real Notion workspace modifications.

Mitigation: Use a least-privilege Notion integration shared only with intended pages or databases, and review create or append commands before execution.

## Reference(s):

- [Notion API Reference](references/notion-api.md)
- [Notion REST API base endpoint](https://api.notion.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell and Python examples; CLI execution returns text or JSON from Notion API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Notion integration token and workspace sharing permissions for the target pages or databases.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
