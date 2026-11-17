## Description:

Manages a Mopidy music service on a NAS, including playback status, playback controls, volume changes, playlist viewing, and local library scans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jesson1222-ship-it](https://clawhub.ai/user/jesson1222-ship-it)

### License/Terms of Use:

MIT

## Use Case:

Users managing a Mopidy-backed NAS music service use this skill to check player state, control playback workflows, adjust volume, inspect playlists, and scan a local music library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe recursive permission guidance could weaken NAS music directory access controls.

Mitigation: Avoid chmod -R 777; use owner/group-specific permissions for the Mopidy container.

Risk: Restart and local scan commands affect the running Mopidy service.

Mitigation: Run administrative commands only when you intend to affect that service and have confirmed the target container.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jesson1222-ship-it/skills/lu-music-player)
- [Publisher profile](https://clawhub.ai/user/jesson1222-ship-it)
- [Source homepage](https://github.com/openclaw/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and service URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include administrative Docker commands for the configured Mopidy service.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, artifact/_meta.json, artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
