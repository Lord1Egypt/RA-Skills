## Description:

Control Sonos speakers (discover/status/play/volume/group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

People using an AI agent can discover Sonos speakers on their local network and manage playback, volume, groups, favorites, and queues through the Sonos CLI. They can also search music services and get troubleshooting guidance when speaker discovery fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Control commands can change playback, volume, speaker grouping, or queued content on the local Sonos system.

Mitigation: Confirm the intended speaker or group and requested change before running a control command.

## Reference(s):

- [Sonos CLI homepage](https://sonoscli.sh)
- [Sonos CLI Go install package](https://pkg.go.dev/github.com/steipete/sonoscli/cmd/sonos)
- [ClawHub skill release](https://clawhub.ai/hillstreet-ph/skills/oc-sonoscli)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands address the selected Sonos speaker or group; Spotify Web API search is optional and requires client credentials.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
