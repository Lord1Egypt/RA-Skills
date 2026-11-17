## Description:

Notify the user before starting noticeable long-running tasks, provide configurable progress heartbeats, and send immediate completion or failure notices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fogyoy](https://clawhub.ai/user/fogyoy)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when an agent starts a task expected to take more than 2-3 minutes, so the agent sends a start notice, periodic progress updates, and an immediate completion or failure message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to restart a gateway if heartbeat cleanup remains stuck.

Mitigation: Prefer removing or overriding the gateway-restart behavior and limit cleanup to retrying heartbeat removal or scheduling a bounded cleanup job.

Risk: Heartbeat jobs may continue sending progress messages if cleanup fails.

Mitigation: Prefer in-run heartbeat messages when possible; when cron is used, store the heartbeat job ID and remove it in both success and failure paths.

Risk: Notification text may not match the user's preferred language.

Mitigation: Confirm or adapt notification messages to the user's preferred language before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fogyoy/skills/let-me-know)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown status messages with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default heartbeat interval is 5 minutes and can be changed by the user.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
