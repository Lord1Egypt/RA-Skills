## Description:

Configures a stable, maintainable OpenClaw rescue gateway with a separate Discord bot, port, launchd label, workspace, and execution posture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cchaojiejes](https://clawhub.ai/user/cchaojiejes)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure a persistent OpenClaw rescue gateway that remains separate from the main gateway. It covers rescue bot setup, launchd service isolation, profile paths, validation commands, and day-to-day operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends a persistent Discord-connected rescue gateway with full local command authority and approval prompts disabled.

Mitigation: Install only when that posture is deliberate; prefer scoped rescue credentials, restrict Discord users and channels, and keep command approval enabled where possible.

Risk: Copying primary agent auth profiles into the rescue agent can broaden credential exposure.

Mitigation: Use separate low-privilege rescue credentials where possible and document token revocation procedures before deployment.

Risk: A custom LaunchAgent can keep the rescue gateway running persistently after emergency use.

Mitigation: Document stop commands, LaunchAgent removal steps, and token revocation as part of operational runbooks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cchaojiejes/skills/openclaw-rescue-gateway-skill)
- [Publisher Profile](https://clawhub.ai/user/cchaojiejes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw profile settings, launchd service guidance, operational commands, and credential-handling guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
