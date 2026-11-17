## Description:

Atomic node skill to initialize a Gmail draft with recipients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create a new Gmail draft addressed to specified recipients, leaving the subject and body for separate update skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent Gmail drafts through the gog CLI.

Mitigation: Require review before installation and use only where the agent is allowed to create Gmail drafts.

Risk: Recipient values may be passed through a broadly triggered shell command without clear confirmation or validation.

Mitigation: Require explicit confirmation of the recipient list and prefer structured process arguments over shell interpolation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/gmail-draft-initialize)

## Skill Output:

**Output Type(s):** [shell commands, JSON]

**Output Format:** [JSON response from the Gmail draft creation command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates an empty Gmail draft with recipients only and returns a draft ID.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
