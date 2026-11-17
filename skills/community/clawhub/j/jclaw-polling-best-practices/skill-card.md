## Description:

Guides agents through cron-style polling for long-running asynchronous CLI commands or API jobs with machine-checkable completion conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skywalker-lili](https://clawhub.ai/user/skywalker-lili)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to decide when polling fits a long-running task, confirm parameters, create task and progress files, adapt a polling shell script, and notify or trigger follow-up work after completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad background shell execution can run unintended or stale commands if task scope is not explicitly confirmed.

Mitigation: Use only trusted, user-confirmed polling tasks and require clear parameters, owner, timeout, log location, and cancellation path before launch.

Risk: The executable template uses eval-style command and parser hooks that can be unsafe with untrusted inputs.

Mitigation: Replace eval-based template logic with fixed commands or allowlisted parsers before using the script.

Risk: Background polling jobs can outlive the initiating agent session and continue consuming resources.

Mitigation: Avoid upstream auto-starts and ensure each job records progress, errors, timeout behavior, notification target, and cleanup expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skywalker-lili/skills/jclaw-polling-best-practices)
- [Publisher profile](https://clawhub.ai/user/skywalker-lili)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled shell template is generic and must be adapted with user-confirmed commands, completion conditions, timeouts, notification targets, and post-poll actions before execution.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
