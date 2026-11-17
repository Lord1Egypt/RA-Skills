## Description:

Manage Jotform forms, submissions, labels, and user accounts. Create and clone forms, retrieve submissions and reports, manage form labels, and monitor account usage and settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect a Jotform account through ClawLink, inspect forms and submissions, manage labels, generate reports, and perform confirmed account or form changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on ClawLink and its hosted OAuth flow to access the connected Jotform account.

Mitigation: Install only if the publisher and ClawLink service are trusted, and review the plugin source, version, and OAuth scopes where available.

Risk: Read operations can expose Jotform submission data and account details.

Mitigation: Handle returned submission and account data according to applicable privacy and data handling policies.

Risk: Write actions can change labels, settings, or cloned forms in the connected Jotform account.

Mitigation: Use previews and execute write or destructive operations only after the user confirms the target resource and intended effect.

## Reference(s):

- [Jotform API Documentation](https://api.jotform.com/docs/)
- [Jotform Form Management](https://www.jotform.com/form-management/)
- [ClawLink for OpenClaw](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON parameters for Jotform tool calls and confirmation prompts for write actions.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
