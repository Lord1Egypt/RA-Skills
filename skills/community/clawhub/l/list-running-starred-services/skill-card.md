## Description:

Runs `bytedcli tce list-starred-service` and prints the raw original output directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plusplus7](https://clawhub.ai/user/plusplus7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators with access to a local bytedcli environment use this skill to list TCE starred services and review the raw command output in the agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw starred-service output may expose service names or account-context details in the conversation.

Mitigation: Install and invoke the skill only where sharing raw bytedcli output is appropriate, and review the output before redistributing it.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Text]

**Output Format:** [Plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Raw bytedcli output is printed directly without filtering or post-processing.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
