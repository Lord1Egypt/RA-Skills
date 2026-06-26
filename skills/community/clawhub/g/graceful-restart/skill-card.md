## Description: <br>
Restarts OpenClaw Gateway by scheduling a one-time wakeup message to the main session so task context can resume after the restart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scotthuang](https://clawhub.ai/user/scotthuang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill when Gateway needs to restart without leaving the main session stalled; it creates a one-time resume event, restarts Gateway, and relies on OpenClaw to deliver the wakeup message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad trigger such as "restart" or "重启" could restart Gateway from an ambiguous user request. <br>
Mitigation: Require explicit restart intent, such as "restart Gateway" or "重启 Gateway", and ask for confirmation before running the skill on vague restart requests. <br>
Risk: The skill requires permission to restart Gateway and create a one-time OpenClaw cron event. <br>
Mitigation: Install it only for agents and workspaces where Gateway restart and cron scheduling are intended capabilities. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scotthuang/graceful-restart) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Configuration] <br>
**Output Format:** [CLI status output and an OpenClaw system-event message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the openclaw CLI; default wakeup delay is 10 seconds unless --delay is provided.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
