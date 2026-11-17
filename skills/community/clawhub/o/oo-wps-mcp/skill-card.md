## Description:

WPS MCP (wps.cn). Use this skill for ANY WPS MCP request — reading, creating, updating, and deleting data. Whenever a task involves WPS MCP, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to read, search, create, and manage WPS cloud documents, spreadsheets, PDFs, and folders through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute unverified downloaded code without a separate approval step.

Mitigation: Verify and install the CLI separately before use, and require approval for local setup changes.

Risk: Automatic skill synchronization could modify agent configurations.

Mitigation: Review synchronization behavior before allowing it to change agent configurations.

Risk: WPS write or deletion actions can change user data.

Mitigation: Require explicit confirmation for edits and deletions.

## Reference(s):

- [ClawHub release](https://clawhub.ai/oomol/skills/oo-wps-mcp)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [WPS](https://www.wps.cn)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Files]

**Output Format:** [Shell commands with JSON payloads; WPS content may be returned as Markdown, plain text, or structured data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read and create or modify WPS content; write and destructive actions require explicit confirmation.]

## Skill Version(s):

1.0.5 (source: release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
