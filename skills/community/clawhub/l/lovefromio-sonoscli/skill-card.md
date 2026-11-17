## Description:

Control Sonos speakers (discover/status/play/volume/group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovefromio](https://clawhub.ai/user/lovefromio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to control Sonos speakers on a local network, including discovery, playback, volume, grouping, favorites, queue management, and optional Spotify search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install metadata fetches and builds an unpinned third-party Go CLI dependency at install time.

Mitigation: Pin or review a specific sonoscli module version before installing when stronger supply-chain control is required.

Risk: Spotify search requires credentials when that optional feature is used.

Mitigation: Provide Spotify credentials only when Spotify search is needed, and manage those credentials through the agent runtime's normal secret-handling process.

## Reference(s):

- [Sonos CLI homepage](https://sonoscli.sh)
- [sonoscli Go install module](https://pkg.go.dev/github.com/steipete/sonoscli/cmd/sonos)
- [ClawHub skill page](https://clawhub.ai/lovefromio/skills/lovefromio-sonoscli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes the sonos CLI is installed and available as the sonos binary.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
