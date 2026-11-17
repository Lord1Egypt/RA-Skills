## Description:

Helps Go developers create minimal or standard golangci-lint configurations and troubleshoot common local or CI lint failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers working on personal Go projects use this skill to select golangci-lint templates, prepare .golangci.yml content, run lint commands, and troubleshoot import, type-checking, or CI failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructions claim broader powers than a Go lint configuration helper needs.

Mitigation: Use the skill only for golangci-lint configuration and troubleshooting, and disregard unrelated project-management or broad workflow claims.

Risk: The skill may ask the agent to write .golangci.yml files or run installation and lint commands.

Mitigation: Review proposed file changes and commands before allowing writes or execution, especially install commands and CI-related shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/go-linter-config-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose .golangci.yml content and lint commands for user review before file writes or execution.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
