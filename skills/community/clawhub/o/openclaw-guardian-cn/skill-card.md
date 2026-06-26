## Description: <br>
OpenClaw Guardian CN monitors OpenClaw Gateway health, checks skills, channels, plugins, and system resources, and can attempt configured recovery actions such as restarting the Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenbinxin](https://clawhub.ai/user/shenbinxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to run scheduled or manual health checks, detect Gateway and plugin issues, and receive recovery-oriented guidance or commands for restoring service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can set up persistent watchdog tasks and scheduled execution for OpenClaw monitoring. <br>
Mitigation: Review cron or Windows Task Scheduler commands before enabling them, verify the referenced scripts and paths, and keep removal steps and log locations available. <br>
Risk: Some Windows scheduled-task examples use elevated execution. <br>
Mitigation: Avoid elevated setup unless it is required for the local OpenClaw installation and approved by the operator. <br>
Risk: Automatic recovery commands may restart or start the OpenClaw Gateway. <br>
Mitigation: Run the checks manually first, confirm the target OpenClaw command and installation path, and verify recovery results after each action. <br>


## Reference(s): <br>
- [OpenClaw Guardian CN on ClawHub](https://clawhub.ai/shenbinxin/openclaw-guardian-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status reports with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
