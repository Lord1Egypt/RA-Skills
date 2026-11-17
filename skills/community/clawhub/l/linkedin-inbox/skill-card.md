## Description:

LinkedIn inbox management with scheduled scanning, auto-draft responses following user's communication style, and approval workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dylanbaker24](https://clawhub.ai/user/dylanbaker24)

### License/Terms of Use:


## Use Case:

People who manage LinkedIn messages use this skill to scan inbox activity, draft replies in their own communication style, and route proposed responses through approval before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private LinkedIn messages through an active browser session.

Mitigation: Use a dedicated browser profile or account, restrict notification channels, and avoid retaining inbox screenshots unless necessary.

Risk: The included send workflow can send LinkedIn messages without strong built-in approval or recipient verification controls.

Mitigation: Require an explicit approval token, verify the recipient before sending, apply rate limits, and use fail-closed UI checks before relying on the send script.

## Reference(s):

- [Communication Style Extraction Guide](references/style-extraction.md)
- [LinkedIn Inbox Manager on ClawHub](https://clawhub.ai/dylanbaker24/skills/linkedin-inbox)
- [LinkedIn Messaging](https://www.linkedin.com/messaging/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces inbox summaries, draft responses, approval prompts, and browser automation commands for an agent to execute with user oversight.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
