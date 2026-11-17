## Description:

Helps OpenClaw users create and manage chat-capable digital humans on the PowPow map and respond to visitors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can set up a PowPow digital human, manage its account and subscriptions, and review or reply to map visitors' messages. An optional companion channel plugin enables ongoing conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable account and digital-human webhook tokens are stored in a local plaintext credentials file and shown in terminal output.

Mitigation: Use a private machine and account; protect the credentials file and copied plugin configuration as secrets, and never commit or share them.

## Reference(s):

- [PowPow Agent on ClawHub](https://clawhub.ai/durenzidu/skills/powwow-agent)
- [PowPow map](https://global.powpow.online/map)
- [PowPow channel plugin on ClawHub](https://clawhub.ai/durenzidu/plugins/openclaw-channel-powpow)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Text and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes account status, digital-human details, visitor chat history, and plugin setup guidance.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
