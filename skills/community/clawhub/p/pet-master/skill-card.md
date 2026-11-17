## Description:

Adopt and care for a MagicHaqi virtual pet by logging into the real browser game, reading pet state, and sending care, chat, adoption, shop, and sharing commands with human confirmation for sensitive actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paraengine](https://clawhub.ai/user/paraengine)

### License/Terms of Use:

MIT-0

## Use Case:

External MagicHaqi users can delegate routine virtual-pet adoption, care, chat, and sharing workflows to an agent. The skill is intended for assisted game interaction where the human confirms adoption, purchases, host choice, and other sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to handle KeepWork login credentials and session tokens, including tokenized URLs.

Mitigation: Use only a known official MagicHaqi host, avoid placing credentials or tokens in logs or screenshots, and prefer interactive login when token handling cannot be contained.

Risk: A user-supplied host could receive an account token if the agent opens a tokenized MagicHaqi URL on the wrong site.

Mitigation: Confirm the host with the human before opening tokenized URLs and do not use unknown or unexpected hosts.

Risk: Adoption binds an agent owner and shop purchases spend in-game coins.

Mitigation: Require explicit human confirmation before adoption or purchases, then re-read state after each write command.

Risk: Pet chat can save memory lines and may retain information the user shares.

Mitigation: Avoid sending personal or sensitive information through pet chat.

## Reference(s):

- [MagicHaqi Agent Commands](artifact/commands.md)
- [MagicHaqi Agent Integration](artifact/integration.md)
- [ClawHub Skill Page](https://clawhub.ai/paraengine/skills/pet-master)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration, shell commands]

**Output Format:** [Markdown with HTTP examples, URL patterns, and JSON command payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read-first command workflow, requestId correlation, and screenshot or state confirmation guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
