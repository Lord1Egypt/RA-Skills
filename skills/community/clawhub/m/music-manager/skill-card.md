## Description:

Music Manager downloads audio from YouTube or Bilibili, converts it to MP3, and organizes files in a local music library by category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2771096196](https://clawhub.ai/user/2771096196)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to find or download music from YouTube or Bilibili, convert it to MP3, and store it under a chosen local category.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader reads Chrome browser cookies by default for yt-dlp authenticated downloads.

Mitigation: Set BROWSER = None before use unless authenticated downloads are required, and review whether browser-cookie access is acceptable for the environment.

Risk: Untrusted category names can redirect downloaded files outside the intended music folder.

Mitigation: Use reviewed, trusted category names and confirm the printed download destination before running the download.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2771096196/skills/music-manager)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local MP3 files produced by the download script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local yt-dlp and ffmpeg installation; authenticated downloads may use browser cookies when enabled.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
