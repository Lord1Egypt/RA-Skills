## Description:

Simple video downloader for Jable.tv. Download videos by ID or search by actress name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hs9021401](https://clawhub.ai/user/hs9021401)

### License/Terms of Use:


## Use Case:

External users use this skill to download Jable.tv adult media by video ID or actress search and save the resulting files into organized local folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader can be steered to contact non-Jable URLs and pass unvalidated remote media URLs into a local downloader.

Mitigation: Restrict inputs to known Jable video IDs or Jable.tv URLs until the publisher adds URL and media validation.

Risk: The skill downloads adult media, creates local folders, uses external tools, and makes network requests.

Mitigation: Use a dedicated output folder, confirm the user is comfortable with this media category, and prefer pinned trusted installations of yt-dlp and ffmpeg.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hs9021401/skills/jable-downloader-lite)
- [Jable.tv](https://jable.tv/)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Console status text from shell execution and downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses yt-dlp, ffmpeg, and network access; saves files under the local Videos directory or a requested output directory.]

## Skill Version(s):

1.0.3 (source: server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
