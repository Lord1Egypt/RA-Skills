## Description:

Configure multiple messaging platform accounts for OpenClaw, including Telegram, WhatsApp, Discord, Slack, Signal, and other supported channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devilsen](https://clawhub.ai/user/devilsen)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to add or update messaging channel accounts, collect credential details, merge them into gateway configuration, and verify the resulting setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messaging bot tokens or pairing credentials could be exposed during configuration.

Mitigation: Treat all credentials as secrets, avoid logging or echoing token values, and review responses before sharing them.

Risk: Gateway access settings could permit broader group access than intended.

Mitigation: Confirm the full configuration before applying it and replace open group access with a restrictive policy unless unrestricted access is required.

Risk: Applying configuration changes in the wrong session could affect active messaging accounts.

Mitigation: Use the skill only in an admin setup session and verify the target accounts and bindings before patching the gateway configuration.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration snippets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include gateway configuration guidance involving messaging bot credentials and access policy settings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
