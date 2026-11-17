## Description:

Control whole-house music scenes combining Spotify playback with Airfoil speaker routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and home automation operators use this skill to ask an agent for macOS-based Spotify and Airfoil music scenes such as morning, party, chill, reading, off, and status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls Spotify playback and Airfoil speaker routing on macOS, so broad or accidental triggers could change home-audio state unexpectedly.

Mitigation: Use it only where macOS Spotify and Airfoil control is intended, and narrow the trigger phrases if accidental activation would be disruptive.

Risk: The documented install path includes an optional sudo symlink that exposes the command globally.

Mitigation: Skip the global symlink unless it is needed, or install it only after reviewing the script path and local permissions.

Risk: The reading scene references Living Room and Bedroom speakers that are not listed in the configured speaker inventory.

Mitigation: Confirm and correct Airfoil speaker names before using the reading scene.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/home-music-terry)
- [Publisher Profile](https://clawhub.ai/user/terrycarter1985)
- [Spotify](https://spotify.com)
- [Airfoil](https://rogueamoeba.com/airfoil/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and scene names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces macOS home-audio control guidance and commands for Spotify and Airfoil scenes.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
