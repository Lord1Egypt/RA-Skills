## Description:

Provides human-help support to AI agents through HeySummon by monitoring help requests, sending provider notifications, and forwarding provider replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomasansems](https://clawhub.ai/user/thomasansems)

### License/Terms of Use:


## Use Case:

Developers and operators who act as human-help providers use this skill to receive AI-agent support requests through HeySummon and respond from a messaging app or reply script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts a persistent background watcher.

Mitigation: Run the teardown script when the watcher is no longer needed.

Risk: The skill reads local HeySummon and OpenClaw credentials and stores raw event history locally.

Mitigation: Protect the .env file and local event logs, and use an HTTPS HeySummon URL for any non-local service.

Risk: Replies can be forwarded automatically through HeySummon.

Mitigation: Avoid sending sensitive content through automatic replies.

## Reference(s):

- [HeySummon](https://heysummon.ai)
- [ClawHub skill page](https://clawhub.ai/thomasansems/skills/heysummon-provider)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and helper script invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a persistent watcher and sends notification and reply content through HeySummon.]

## Skill Version(s):

0.1.0-beta (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
