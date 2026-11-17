## Description:

Guides agents through connecting Claude or OpenClaw to Notion, Linear, Slack, and GitHub with MCP setup checklists, configuration templates, tests, and troubleshooting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flynndavid](https://clawhub.ai/user/flynndavid)

### License/Terms of Use:


## Use Case:

Developers, operators, and technical teams use this skill to configure MCP server connections for productivity tools, validate that Claude can use those tools, and troubleshoot setup failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable third-party MCP server packages, including npx and uvx commands.

Mitigation: Review packages before installing, pin exact MCP server versions from trusted publishers, and test in non-production environments first.

Risk: The setup uses powerful Slack, Notion, GitHub, and Linear tokens that may allow agents to read or modify connected systems.

Mitigation: Grant the narrowest token scopes possible and avoid connecting production workspaces or repositories unless that access is acceptable.

Risk: The validation prompts include live write actions such as creating pages, issues, or messages.

Mitigation: Run write tests only in sandbox workspaces, test channels, or disposable repositories, and review results before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flynndavid/skills/mcp-server-setup-kit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration snippets, bash commands, checklists, prompts, and troubleshooting steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance and templates for MCP connections; it does not itself provision services or credentials.]

## Skill Version(s):

1.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
