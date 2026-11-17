## Description:

Helps agents discover, select, and call MCP tools through a compact catalog, and provides workflows for managing tool and skill configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[activeing123](https://clawhub.ai/user/activeing123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to find and call the right MCP tools with less catalog overhead, and to manage agent tool and skill configurations. It also helps agents identify relevant documentation and understand compressed tool results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation rules may lead to software installation or execution before the user is informed.

Mitigation: Get explicit approval before installation or execution, and use a reviewed package version in an isolated environment.

Risk: Tool and skill synchronization can change local agent configuration, and cached tool results may contain sensitive information.

Mitigation: Preview configuration and synchronization changes, retain backups, use the documented restore workflow when undoing routing changes, and set cache expiry when results are sensitive.

## Reference(s):

- [Clawhub skill release](https://clawhub.ai/activeing123/skills/mcptoon)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, MCP tool calls]

**Output Format:** [Markdown with shell command examples and JSON arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend local installation or agent configuration changes; request approval before making changes.]

## Skill Version(s):

1.0.14 (source: server-resolved release; artifact frontmatter lists 1.4.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
