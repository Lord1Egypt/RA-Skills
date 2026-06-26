## Description: <br>
Runs long-running agent tasks in the background, tracks progress, and sends periodic status and completion notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankieway](https://clawhub.ai/user/frankieway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep builds, deployments, migrations, model training, and other long-running commands from blocking the main interaction while progress and completion updates are delivered. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send raw command output and logs to messaging channels. <br>
Mitigation: Use it only with trusted background jobs and recipients, and configure notifications to send status-only or sanitized summaries when commands may expose credentials, customer data, private logs, deployments, or database migrations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/frankieway/long-task-handler) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown status messages with command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task summaries, progress excerpts, exit codes, timeout notices, and completion notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact _meta.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
