## Description:

Control Music Assistant (Home Assistant music server) - playback, volume, queue management, and library search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rodrigosiviero](https://clawhub.ai/user/rodrigosiviero)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to control a configured Music Assistant server, including playback, volume, queue management, library search, player status, and library sync operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a long-lived bearer token against a user-configured Music Assistant endpoint that is documented with plaintext HTTP examples.

Mitigation: Use HTTPS or a trusted local-only connection, protect MA_TOKEN as a secret, prefer a dedicated low-scope token if supported, and rotate the token if it may have crossed an untrusted network.

Risk: Direct API commands and playback or queue actions can immediately affect the active listening session.

Mitigation: Confirm the target player and command before issuing playback, queue, volume, sync, or direct JSON-RPC operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rodrigosiviero/skills/music-assistant)
- [Music Assistant API documentation on configured server](http://YOUR_SERVER:8095/api-docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MA_URL and MA_TOKEN environment variables; MA_PLAYER is optional.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
