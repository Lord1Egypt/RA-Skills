## Description:

Message Hub - AI Team Message Hub Client for async collaboration

This skill is ready for commercial/non-commercial use.

## Publisher:

[socneo](https://clawhub.ai/user/socneo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-team operators use this skill to configure a Python client that sends, pulls, broadcasts, and checks messages through a Tianma Message Hub endpoint for asynchronous collaboration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and message contents can be exposed if the Message Hub endpoint is not controlled or traffic is sent over plain HTTP.

Mitigation: Use only trusted endpoints, require HTTPS for non-local deployments, store credentials in environment variables, rotate keys, and avoid sending secrets in messages.

Risk: The artifact claims message signature verification, but the security evidence says that claim should not be relied on by itself.

Mitigation: Require the server or a downstream client to independently verify message authenticity before acting on received messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/socneo/skills/message-hub-socneo)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on configuring environment variables, using the Python client, and invoking the CLI against a Message Hub endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
