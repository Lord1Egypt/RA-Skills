## Description:

Downloads videos, audio, and Pinterest images from supported links into local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to save media from links or gather Pinterest images for moodboards and visual references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated downloads can send applicable browser-session cookies to the relevant remote service.

Mitigation: Clearly disclose this before use and get the user's approval before using browser-session authentication.

Risk: The video helper may fetch and run an unpinned standalone yt-dlp build on first use.

Mitigation: Use a version-pinned installer and dependency setup before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vargai/skills/media-download)
- [Project homepage (metadata/clawdis)](https://github.com/vargHQ/skills/tree/main/media-download)
- [Pinterest moodboard presets](artifact/references/pinterest-presets.md)
- [yt-dlp installation documentation](https://github.com/yt-dlp/yt-dlp#installation)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [Local video, audio, and image files with saved file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads are saved locally; available formats depend on the source and selected options.]

## Skill Version(s):

1.0.8 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
