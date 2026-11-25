## Description:

Use this skill to work with WPS cloud files through a connected WPS MCP account, including searching, reading, creating, and managing documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users can search, read, and manage WPS cloud files using their connected account. Review the action schema first, and confirm before running actions marked as writes or destructive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial and reports a suspicious setup step that runs a remote installer whose contents were not inspected.

Mitigation: Verify the installer source and review what it changes before installing; the available scan does not establish that the skill is safe.

## Reference(s):

- [WPS MCP ClawHub release](https://clawhub.ai/oomol/skills/oo-wps-mcp)
- [WPS](https://www.wps.cn)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Text, Files]

**Output Format:** [Structured JSON results, Markdown or plain-text document content, and file download information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available content and actions depend on the selected WPS MCP action and file type.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
