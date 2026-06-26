## Description: <br>
Audit and optimize OpenClaw token usage, cron job efficiency, and agent performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrmps](https://clawhub.ai/user/mrmps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw cron jobs, session traces, plugin overhead, token consumption, and cost drivers before applying approved efficiency changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects OpenClaw cron configuration, logs, and selected session traces that may contain sensitive operational context. <br>
Mitigation: Run it interactively, review what the agent plans to inspect, and avoid exposing unnecessary logs or traces. <br>
Risk: Optimization proposals may change cron frequency, context loading, session persistence, model choice, or deletion of redundant jobs. <br>
Mitigation: Require explicit approval for each change and keep a rollback plan before edits, deletions, persistent-session changes, or gateway restarts. <br>


## Reference(s): <br>
- [OpenClaw Cron Jobs](https://docs.openclaw.ai/automation/cron-jobs) <br>
- [OpenClaw CLI Reference](https://docs.openclaw.ai/cli) <br>
- [OpenClaw CLI Cron](https://docs.openclaw.ai/cli/cron) <br>
- [OpenClaw Gateway Security](https://docs.openclaw.ai/gateway/security) <br>
- [ClawHub Skill Page](https://clawhub.ai/mrmps/openclaw-optimize) <br>
- [Publisher Profile](https://clawhub.ai/user/mrmps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive recommendations require explicit user approval before configuration changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
