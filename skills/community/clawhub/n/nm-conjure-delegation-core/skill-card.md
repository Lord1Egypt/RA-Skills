## Description:

Delegates execution tasks to external CLIs and providers, including Gemini, Qwen, MiniMax, GLM, Muse, Codex, OpenCode, and Glimmer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to decide which execution work can be delegated to external AI providers, prepare handoffs, estimate costs, and validate returned results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an undeclared MCP server registration capability.

Mitigation: Before installing, review the MCP registration instructions and verify and approve each server and permission.

Risk: The security evidence reports telemetry guidance that may include personal identifiers.

Mitigation: Review telemetry guidance before use and avoid sending personal identifiers unless their collection and handling are approved.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-conjure-delegation-core)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell command examples and delegation plan templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes provider selection, handoff, cost, validation, and troubleshooting guidance.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence; artifact frontmatter lists 1.10.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
