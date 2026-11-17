## Description:

Research-before-coding workflow. Search for existing tools, libraries, and patterns before writing custom code. Invokes the researcher agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill before implementing features, adding dependencies, or creating utilities to compare existing packages, MCP servers, skills, and reference implementations before deciding whether to adopt, extend, compose, or build.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to inspect user-level Claude configuration and installed skills while researching available tools.

Mitigation: Install and use it only when that local configuration review is acceptable for the workspace.

Risk: The workflow can lead to package installation or MCP configuration decisions based on research results.

Mitigation: Require explicit approval before installs or MCP changes, review package source and publisher, pin versions, and prefer sandboxed installs with lifecycle scripts disabled where possible.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
