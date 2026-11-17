## Description:

Play audio/video locally on the host

This skill is ready for commercial/non-commercial use.

## Publisher:

[xejrax](https://clawhub.ai/user/xejrax)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to control local audio and video playback through mpv, including local media files and trusted remote media URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires mpv to be installed through the host system package manager.

Mitigation: Install mpv only on hosts where that dependency is acceptable and review the package-manager change before deployment.

Risk: Playing remote media URLs causes mpv to connect to those media locations.

Mitigation: Use trusted remote media sources and avoid unreviewed URLs.

## Reference(s):

- [Media Player skill listing](https://clawhub.ai/xejrax/skills/media-player)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose media-player commands that rely on mpv being installed on the host.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
