## Description:

NeuralMind helps agents answer repository questions with compact indexed context instead of loading large amounts of raw source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dfrostar](https://clawhub.ai/user/dfrostar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use NeuralMind to navigate unfamiliar codebases, locate definitions and callers, trace architecture, and retrieve compact project context before deciding whether raw source reads are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: NeuralMind indexes the repository and keeps persistent `.neuralmind` state that may be reused by other agents pointed at the same path.

Mitigation: Use it only on repositories where persistent local code index state is acceptable, and review storage practices before using it on private or sensitive codebases.

Risk: The skill installs and invokes the `neuralmind` package and MCP or CLI tooling.

Mitigation: Install it in an isolated environment and pin or review the `neuralmind` package version before use.

## Reference(s):

- [NeuralMind ClawHub skill page](https://clawhub.ai/dfrostar/skills/neuralmind)
- [dfrostar ClawHub publisher profile](https://clawhub.ai/user/dfrostar)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool-result descriptions and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [NeuralMind query tools return JSON envelopes whose context field contains compact Markdown; shell commands are suggested for installation, indexing, and fallback CLI use.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 3.4.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
