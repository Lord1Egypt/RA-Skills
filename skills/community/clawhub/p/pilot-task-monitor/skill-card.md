## Description:

Real-time dashboard for task status and polo score tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators using Pilot Protocol use this skill to monitor active task queues, submitted task status, completion metrics, and polo score changes across agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring commands can display task IDs, requesters, targets, statuses, and polo score information.

Mitigation: Install and run the skill only in Pilot Protocol environments where the agent is authorized to view task and score metadata.

Risk: The dashboard workflow depends on local pilotctl, jq, watch, and a running Pilot daemon.

Mitigation: Confirm those dependencies are installed and use the disclosed read-only commands before relying on the dashboard output.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-task-monitor)

## Skill Output:

**Output Type(s):** [shell commands, markdown, guidance]

**Output Format:** [Markdown with bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, jq, watch, and a running Pilot daemon; commands use read-only monitoring output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
