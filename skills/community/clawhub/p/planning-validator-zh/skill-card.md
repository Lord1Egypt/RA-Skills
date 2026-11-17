## Description:

计划验证器 describes a pre-execution review workflow for checking multi-step agent plans, tool availability, permissions, dependencies, constraints, and user clarification points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as planning guidance before executing complex agent tasks, especially when plans need checks for available tools, permissions, dependencies, constraints, and explicit user clarification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents itself as a pre-execution safety validator, but the bundled validator is mostly a placeholder and may create false assurance.

Mitigation: Treat it as draft planning guidance only; do not use it as an approval gate until it parses real plan files, validates schemas, checks actual tool capabilities and permissions, and fails closed on uncertainty.

Risk: The example reality check returns a fixed successful confidence value instead of testing real plan feasibility.

Mitigation: Require independent review or a real validator implementation before executing plans that depend on this skill's feasibility assessment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/planning-validator-zh)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, text]

**Output Format:** [Markdown guidance with Python examples and simple text or dictionary-style validation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external API calls, credential environment variables, MCP tools, or release-channel URLs were detected in the artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
