## Description:

Control whole-house music scenes combining Spotify playback with Airfoil speaker routing. Quick presets for morning, party, chill modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate predefined whole-house music scenes on macOS by controlling local Spotify playback and Airfoil speaker routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start, stop, route, and change volume for local Spotify and Airfoil playback.

Mitigation: Install it only on macOS systems where local music and speaker control is intended, and review the configured playlists, speaker names, and helper script path before use.

Risk: Broad music-related triggers may activate a scene when the user intended a different music action.

Mitigation: Review trigger phrases and keep scene names explicit for deployments where accidental playback or speaker routing would be disruptive.

Risk: The documented global symlink installation uses sudo and makes the command available system-wide.

Mitigation: Skip the sudo symlink unless global terminal access is needed, or install the command in a user-owned path.

## Reference(s):

- [Home Music Enhanced ClawHub Page](https://clawhub.ai/terrycarter1985/skills/home-music-enhanced)
- [Spotify](https://spotify.com)
- [Airfoil](https://rogueamoeba.com/airfoil/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and local configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, Spotify Desktop, Airfoil, and a configured spotify-applescript helper path.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
