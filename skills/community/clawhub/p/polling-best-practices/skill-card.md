## Description:

Best practices for automating long-running, asynchronous tasks via cron-style polling when a background CLI command or API call returns a handle and has a clear, machine-parseable completion condition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skywalker-lili](https://clawhub.ai/user/skywalker-lili)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to decide when polling is appropriate, confirm polling parameters, create a resumable temporary task folder, and monitor bounded asynchronous jobs to completion, timeout, or failure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reusable shell template evaluates configurable command strings as shell code.

Mitigation: Replace eval-based command parsing with fixed commands or argument arrays before using the template.

Risk: Polling logs retained under temporary directories may include command output or sensitive task details.

Mitigation: Use private directories for logs, limit logged output, and review retention before starting a polling task.

Risk: Background polling creates temporary folders and bounded shell processes that can outlive the active agent session.

Mitigation: Confirm task parameters, timeout limits, retention expectations, and cleanup steps with the user before launch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skywalker-lili/skills/polling-best-practices)
- [Publisher profile](https://clawhub.ai/user/skywalker-lili)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and bash script templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce polling plans, task metadata schemas, shell snippets, and status notifications.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
