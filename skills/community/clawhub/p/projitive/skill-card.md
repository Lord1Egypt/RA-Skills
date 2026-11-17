## Description:

Projitive is an MCP-first governance skill for agent-driven delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinxulai](https://clawhub.ai/user/yinxulai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to coordinate repository governance tasks, gather project context through Projitive MCP methods, and keep task status changes tied to evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to globally install the mutable third-party MCP package `@projitive/mcp@latest`.

Mitigation: Review the MCP package before installation and prefer a pinned version or controlled local install.

Risk: The skill can initialize `.projitive/` governance files and drive task status updates in a repository.

Mitigation: Use it only in repositories where automatic governance files and evidence-linked task updates are acceptable.

## Reference(s):

- [Projitive ClawHub skill page](https://clawhub.ai/yinxulai/skills/projitive)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands and MCP method names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in .projitive governance files, design notes, reports, and evidence-linked task status updates.]

## Skill Version(s):

2.1.3 (source: ClawHub release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
