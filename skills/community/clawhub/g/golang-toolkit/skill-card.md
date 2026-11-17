## Description:

Go helps agents review and improve Go code by identifying goroutine leaks, interface design traps, concurrency issues, style problems, and dependency risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to write, review, and improve Go code. It focuses on Go source snippets or file paths, especially goroutine leak detection, interface design review, style checks, and concurrency bug guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may read Go source code and use a configured LLM or API service, which can expose sensitive repository content if the environment is not controlled.

Mitigation: Use the skill only in approved repositories, avoid codebases containing secrets, and rely on agent-environment controls that prevent secret disclosure.

Risk: The skill discloses broad agent capabilities, including optional file writes and development command execution.

Mitigation: Review command plans and code diffs before execution, and run the agent with least-privilege filesystem and shell permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/golang-toolkit)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Skill homepage](https://skillhub.cn/skill/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or JSON-style review output with code snippets, recommendations, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts Go code snippets or file paths plus an optional check_type such as leak, interface, style, or all.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
