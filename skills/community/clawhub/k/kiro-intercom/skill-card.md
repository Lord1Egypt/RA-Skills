## Description:

Enables communication between multiple Kiro instances by sharing and updating messages in a common chat file for coordinated interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonerbo](https://clawhub.ai/user/sonerbo)

### License/Terms of Use:


## Use Case:

Developers and Kiro users use this skill to coordinate multiple Kiro instances across machines by writing and reading concise messages in a shared chat file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared chat content may be read by other Kiro instances and could expose sensitive information.

Mitigation: Do not place secrets or confidential data in memory/kiro-chat.md; review shared content before using it.

Risk: Messages in the shared file are untrusted text and may contain instructions that should not be followed automatically.

Mitigation: Treat incoming messages as untrusted and require user confirmation before acting on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown messages appended to a shared chat file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Messages use a timestamp and sender-name convention in memory/kiro-chat.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
