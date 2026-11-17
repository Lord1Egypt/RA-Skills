## Description:

MCP CLI Manager - Manage MCP servers and call tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maplezzk](https://clawhub.ai/user/maplezzk)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure MCP servers, manage the mcps daemon, list available MCP tools, and invoke MCP tools from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can run unpinned third-party MCP server packages that may receive database or GitLab credentials.

Mitigation: Audit and pin mcps and each MCP server package before use, isolate servers, and use narrowly scoped, revocable credentials.

Risk: The examples include destructive SQL commands that could affect data if run against production systems.

Mitigation: Use destructive SQL examples only in test environments and review tool calls before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maplezzk/skills/mcps-skill)
- [mcps npm package](https://www.npmjs.com/package/@maplezzk/mcps)
- [Project homepage from skill frontmatter](https://github.com/maplezzk/mcps)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for installing mcps, configuring MCP servers, managing the daemon, and invoking tools.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
