## Description:

Control Plex Media Server - browse libraries, search, play media, manage playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mephistojb](https://clawhub.ai/user/mephistojb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Plex server operators use this skill to ask an agent for Plex API curl commands that browse libraries, search media, inspect sessions, and manage playback with their configured Plex server and token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Plex token can expose access to a user's Plex server if it is logged, shared, or embedded in URLs.

Mitigation: Keep PLEX_TOKEN private, prefer passing it in an X-Plex-Token header where practical, and revoke the token if exposure is suspected.

Risk: Using a non-HTTPS PLEX_SERVER value can expose Plex requests and tokens on the network.

Mitigation: Configure PLEX_SERVER with HTTPS where available before using generated curl commands.

Risk: Playback commands can affect active Plex clients.

Mitigation: Confirm the target player and user intent before starting playback on a device.

## Reference(s):

- [Plex](https://plex.tv)
- [ClawHub skill page](https://clawhub.ai/mephistojb/skills/plex-skill)
- [Publisher profile](https://clawhub.ai/user/mephistojb)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require a configured PLEX_SERVER value and a private PLEX_TOKEN.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
