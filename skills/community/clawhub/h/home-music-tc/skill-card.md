## Description:

Control whole-house music scenes combining Spotify playback with Airfoil speaker routing. Quick presets for morning, party, chill modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External macOS users use this skill to start, stop, check, and customize whole-house music scenes that combine Spotify playback with Airfoil speaker routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accidental voice triggers could start or stop music scenes unexpectedly.

Mitigation: Use explicit trigger phrases and confirm the requested scene before running commands that control speakers.

Risk: The install instructions use an admin-permission symlink command that could replace an existing /usr/local/bin/home-music entry.

Mitigation: Review the target path before running sudo ln -sf and avoid overwriting an existing command unintentionally.

Risk: The skill controls local Spotify playback and Airfoil speaker routing on the user's Mac.

Mitigation: Install only on intended macOS accounts and verify speaker names, connected devices, and volume levels before use.

## Reference(s):

- [Home Music ClawHub release page](https://clawhub.ai/terrycarter1985/skills/home-music-tc)
- [Spotify](https://spotify.com)
- [Airfoil](https://rogueamoeba.com/airfoil/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command snippets and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-specific; requires Spotify Desktop, Airfoil, and spotify-applescript.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
