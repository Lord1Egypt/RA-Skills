## Description: <br>
Guides agents in setting up user-confirmed, cron-style polling for long-running asynchronous CLI or API tasks with clear machine-parseable completion conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skywalker-lili](https://clawhub.ai/user/skywalker-lili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they need an agent to monitor a background job, record progress, notify the user on completion, failure, or timeout, and optionally hand off a successful result to another workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background pollers can persist after the agent session and continue running local commands. <br>
Mitigation: Require explicit user confirmation, use bounded polling intervals and max poll counts, record the task directory and PID, and make the stop procedure clear before launch. <br>
Risk: Generated polling scripts may execute unsafe commands or carry untrusted command and message inputs. <br>
Mitigation: Inspect the generated poll.sh and task.json before launch, avoid untrusted inputs, quote variables, and keep the polling command narrowly scoped. <br>
Risk: Discord notifications and optional agent chaining can disclose task status or trigger additional work. <br>
Mitigation: Use direct notification for failures and timeouts, keep agent chaining disabled unless explicitly needed, and limit messages to the minimum information required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skywalker-lili/jclaw-polling-best-practices) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON examples and bash script templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task metadata, progress files, logs, notification commands, and a generated polling shell script for the agent to review and adapt.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
