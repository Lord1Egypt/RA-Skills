## Description:

Command-line tool for searching, playing, and controlling Plex Media Server and clients via the Plex API on a local network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akivasolutions](https://clawhub.ai/user/akivasolutions)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to search Plex libraries, start playback, control Plex clients, and inspect media metadata from a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a Plex access token in ~/.plexctl/config.json.

Mitigation: Protect the config file, avoid committing or sharing it, and tighten file permissions before use.

Risk: Client discovery can contact Plex cloud services despite local-only privacy claims.

Mitigation: Use the skill only when Plex cloud discovery is acceptable, and review command behavior before relying on local-only operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/akivasolutions/skills/plex-ctl)
- [Publisher profile](https://clawhub.ai/user/akivasolutions)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Plex server URL, Plex access token, and selected client stored in local configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
