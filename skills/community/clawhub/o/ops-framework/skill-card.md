## Description: <br>
A 0-token jobs and monitoring framework for OpenClaw that runs long-running read tasks through scripts, supports checkpoint and resume workflows, and sends periodic progress and immediate Telegram alerts while blocking write jobs by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zjianru](https://clawhub.ai/user/Zjianru) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to manage long-running OpenClaw tasks through local scripts, structured job configuration, status checks, and Telegram progress or alert messages. It is most useful for scans, inventories, syncs, health checks, and other operational tasks that should not require an agent to continuously monitor progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local monitor can run user-configured jobs and persist local state. <br>
Mitigation: Review every command in ops-jobs.json before use, keep the config writable only by trusted users, and prefer read_only jobs. <br>
Risk: Automatic resume can restart long-running jobs without another manual action. <br>
Mitigation: Leave autoResume disabled unless the task is read-only and explicitly approved for automatic continuation. <br>
Risk: Telegram alerts may expose operational status or sensitive command output to the configured destination. <br>
Mitigation: Confirm the Telegram destination before enabling alerts and avoid placing secrets in status output. <br>
Risk: OS scheduler entries can keep monitoring active after the original task is no longer needed. <br>
Mitigation: Remove the launchd, systemd, or cron entry when monitoring should stop. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Zjianru/ops-framework) <br>
- [OPS_FRAMEWORK.md](OPS_FRAMEWORK.md) <br>
- [README.md](README.md) <br>
- [UPSTREAM.md](UPSTREAM.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON job configuration, and Python monitor code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local operational guidance and artifacts for configuring jobs, validating status commands, running monitor ticks, and sending Telegram alerts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
