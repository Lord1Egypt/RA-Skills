## Description:

Helps an agent search, read, create, and manage content in a Tencent Lexiang knowledge base through its MCP connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lexiang](https://clawhub.ai/user/lexiang)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams with access to Lexiang use this skill to find and analyze knowledge-base material, create and edit pages, and manage files, drafts, and tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can change or delete knowledge-base content.

Mitigation: Confirm the intended target and action before allowing writes, deletions, or reverts.

Risk: Folder syncing or uploads could disclose local files or follow symlinks.

Mitigation: Sync only trusted folders without symlinks and review dry-run upload plans before proceeding.

Risk: Reading MCP configuration can expose access tokens.

Mitigation: Supply company_from directly or obtain it through whoami; avoid routine reads of mcp.json and keep tokens out of chat output.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/lexiang/skills/lexiang-mcp-skill)
- [Lexiang MCP setup](https://lexiangla.com/mcp)
- [Skill reference index](artifact/references/index.md)
- [Knowledge-base search and reading](artifact/references/search.md)
- [File upload and download](artifact/references/files.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown responses with knowledge-base links and occasional command or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create, edit, delete, revert, or upload Lexiang content when authorized.]

## Skill Version(s):

2.2.3 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
