## Description:

Notion via notion-cli - a Rust CLI and MCP server for Notion API 2025-09-03+ with read-only defaults, opt-in write and admin modes, rate limiting, response-size caps, untrusted-source output envelopes, JSONL audit logs, dry-run checks, data-source support, schema mutation, relation wiring, page moves, database updates, and caller identity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xarkstar](https://clawhub.ai/user/0xarkstar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect agents to Notion through the notion-cli MCP server, starting with read-only workspace access and explicitly enabling write or admin workflows only when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may mutate Notion pages, databases, or schemas when write or admin modes are enabled.

Mitigation: Keep the MCP server in read-only mode by default, use least-privilege Notion integration tokens, and enable write or admin flags only for workflows where those changes are intended.

Risk: Returned Notion content may contain untrusted instructions or misleading workspace data.

Mitigation: Keep the untrusted-source output envelope enabled and treat returned content as data for review rather than as instructions to follow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xarkstar/skills/notion-cli-mcp)
- [Project repository](https://github.com/0xarkstar/notion-cli)
- [notion-cli-mcp on crates.io](https://crates.io/crates/notion-cli-mcp)
- [Notion integrations](https://www.notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes read-only defaults, opt-in write/admin modes, least-privilege Notion tokens, audit logs, and untrusted output handling.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
