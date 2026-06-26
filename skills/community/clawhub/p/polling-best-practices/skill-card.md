## Description: <br>
Guides agents through user-confirmed cron-style polling for long-running CLI or API jobs with clear, machine-parseable completion conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skywalker-lili](https://clawhub.ai/user/skywalker-lili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to decide when a long-running asynchronous task should be polled, confirm polling parameters with the user, create a resumable task folder, and monitor completion or timeout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A polling job can repeatedly execute a user-provided command in the background. <br>
Mitigation: Confirm the polling command, parser, interval, timeout, and completion action with the user before launch. <br>
Risk: Status command output or temporary logs may contain sensitive data. <br>
Mitigation: Avoid putting secrets in command arguments, keep logged output minimal, and clean up temporary logs when they are no longer needed. <br>
Risk: Polling can be misapplied to tasks that need real-time interaction or subjective completion judgment. <br>
Mitigation: Use the skill only when completion is clear and machine-parseable, and choose a synchronous or interactive approach otherwise. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skywalker-lili/polling-best-practices) <br>
- [Skill guide](artifact/SKILL.md) <br>
- [Polling script template](artifact/scripts/poll-template.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce user confirmation prompts, task metadata, progress files, logs, and an adapted polling shell script.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
