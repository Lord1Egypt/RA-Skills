## Description:

Meeting Score helps a meeting host create Feishu Bitable agenda scoring tables, collect independent H/M/L judge scores, and summarize average scores by agenda item.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixiaojie-1012](https://clawhub.ai/user/lixiaojie-1012)

### License/Terms of Use:


## Use Case:

Meeting hosts use this skill to set up structured agenda scoring in Feishu Bitable, let judges score independently, and produce ranked summary reports after or during a meeting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic calculation can keep polling Feishu tables after the meeting if it is not stopped.

Mitigation: Use automatic calculation only when needed, record the created job ID, stop it after the meeting, and confirm the task is disabled.

Risk: The skill needs Feishu Bitable access and can delete default fields or empty records during initialization.

Mitigation: Limit access to the intended meeting tables and review field or record deletion targets before initialization.

Risk: Judge privacy depends on manually configured Feishu row-level permissions and matching judge names.

Mitigation: Have the host configure advanced permissions before scoring begins and verify judge names match Feishu display names or member fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lixiaojie-1012/skills/meeting-score)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance and structured Feishu Bitable updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates Feishu Bitable tables and can start a polling-based calculation workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
