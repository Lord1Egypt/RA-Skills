## Description:

Atomic node skill to read a specific email via Gmail using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized workspace users use this skill when an agent needs to retrieve the full contents, headers, and metadata of a specific Gmail message by message ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose the full contents and metadata of a Gmail message through configured gog access.

Mitigation: Use it only for authorized messages and confirm the requested message ID before retrieval.

Risk: Retrieved email bodies and headers may contain sensitive information.

Mitigation: Avoid unnecessary logging of raw email content, and redact or summarize sensitive details where practical.

Risk: The skill depends on the local gog CLI and its configured Gmail access.

Mitigation: Install and configure gog with the minimum Gmail access needed for the intended authorized workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/gmail-retrieve-email)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown instructions with an inline shell command and JSON output expectation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI and returns Gmail message headers, body, and metadata for the requested message.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
