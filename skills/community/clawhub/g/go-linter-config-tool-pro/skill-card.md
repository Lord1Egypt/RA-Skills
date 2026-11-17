## Description:

Helps developers and teams create and maintain shared golangci-lint baselines, custom rule and exemption policies, CI matrix workflows, quality gates, and lint trend reporting for Go repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering teams, and automation maintainers use this skill to standardize Go lint configuration across multiple repositories, generate CI lint workflows, and define quality gate and regression tracking practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CI workflows or command suggestions may download modules, use repository tokens, access remote baselines, or change quality gate behavior.

Mitigation: Review generated workflows, commands, remote baseline references, and token usage before applying them to a repository or CI environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/go-linter-config-tool-pro)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with YAML, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce golangci-lint configuration snippets, CI workflow templates, quality gate scripts, and implementation guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
