## Description:

Posts text, media, and scheduled content to supported social media platforms through a multi-provider social posting API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to check connected social accounts, prepare platform-appropriate content, and publish or schedule posts across supported social channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can publish or schedule content to connected public social accounts.

Mitigation: Require a preview and explicit confirmation before executing posting commands, and verify the selected platforms and accounts first.

Risk: The documented inline python -c pattern can execute injected content if user-supplied post text is pasted into the command.

Mitigation: Use a fixed script, stdin, JSON, or argument-array execution so post content is handled as data rather than executable code.

Risk: The skill depends on API keys for third-party posting providers.

Mitigation: Keep provider keys in the environment or a local .env file, limit their account permissions where possible, and rotate them if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-social-post)
- [Canlah AI](https://canlah.ai)
- [PostForMe dashboard](https://postforme.dev/dashboard)
- [LATE dashboard](https://getlate.dev/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in API calls that publish or schedule content when the generated commands are executed.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
