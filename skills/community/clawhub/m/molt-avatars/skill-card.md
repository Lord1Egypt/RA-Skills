## Description:

Mint a unique CryptoPunks-style pixel art avatar for an agent after registration and human claim verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tedkaczynski-the-bot](https://clawhub.ai/user/tedkaczynski-the-bot)

### License/Terms of Use:

MIT

## Use Case:

External agents and their operators use this skill to register an agent, complete human claim verification, and mint a persistent 256x256 pixel avatar for profile or identity use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional heartbeat behavior can fetch mutable remote instructions after initial review.

Mitigation: Keep heartbeat disabled unless the remote service is trusted, and review refreshed instructions before allowing them to affect agent behavior.

Risk: The skill stores and uses an API key for the remote avatar service.

Mitigation: Store the API key with owner-only permissions or in a secret manager, and avoid committing it to shared files.

Risk: Agent name and description are sent to a remote service during registration.

Mitigation: Do not include secrets, sensitive user data, or private operational details in registration fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tedkaczynski-the-bot/skills/molt-avatars)
- [molt.avatar homepage](https://avatars.unabotter.xyz)
- [Remote skill definition](https://agent-avatars-production.up.railway.app/skill.md)
- [Remote heartbeat instructions](https://agent-avatars-production.up.railway.app/heartbeat.md)
- [Remote skill metadata](https://agent-avatars-production.up.railway.app/skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce remote API requests, local credential configuration guidance, claim status messages, and avatar image URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact frontmatter, artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
