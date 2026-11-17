## Description:

Downloads the main video from a Pinterest pin or pin.it short link and saves it as a local MP4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hekaiii](https://clawhub.ai/user/hekaiii)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to retrieve the primary video from a Pinterest pin for personal media workflows such as wallpaper saving, repost preparation, or Live Photo conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can fetch media from an arbitrary URL supplied to the script.

Mitigation: Constrain use to Pinterest pin URLs, pin.it redirects, or expected pinimg HLS media URLs before running ffmpeg.

Risk: The helper can overwrite any writable output path passed to it.

Mitigation: Save only under the intended downloads directory and avoid replacing existing files unless the user explicitly chooses to replace them.

Risk: The skill runs ffmpeg against network media and writes a local MP4.

Mitigation: Review the resolved media URL and verify the saved file before forwarding or reusing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hekaiii/skills/pinterest-video-download)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with local file paths and shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or points to a local MP4 saved under the intended downloads directory.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
