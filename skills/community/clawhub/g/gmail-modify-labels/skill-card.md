## Description:

Atomic node skill to modify email labels in Gmail using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs to add, remove, or change labels on selected Gmail messages or threads through the configured gog CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change labels on the wrong Gmail message, thread, or account if identifiers, targets, labels, or the configured gog account are incorrect.

Mitigation: Confirm the intended Gmail account, message IDs, thread targets, and label names before allowing the command to run.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zvirb/skills/gmail-modify-labels)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with inline shell command and JSON example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns confirmation that labels were updated, or reports the command error after retries.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
