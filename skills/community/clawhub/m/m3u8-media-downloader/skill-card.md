## Description:

Use @lzwme/m3u8-dl for media download and video info parsing when a user provides a video or music URL, including m3u8/HLS, mp4, mp3, and supported sharing links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renxia](https://clawhub.ai/user/renxia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to guide media download, video information parsing, batch download, WebUI operation, and Node API usage through the pinned @lzwme/m3u8-dl CLI and ffmpeg.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a pinned third-party npm CLI and a local ffmpeg installation.

Mitigation: Install only after trusting @lzwme/m3u8-dl@1.9.0 and ffmpeg, and run downloads in a sandbox or limited download directory.

Risk: The optional WebUI can expose download controls if run without an appropriate secret or network boundary.

Mitigation: Keep the WebUI local or otherwise restricted, and configure a strong DS_SECRET or token before exposure.

Risk: Media downloads may violate source site terms or local law if used on unauthorized content.

Mitigation: Use the skill only for media the user is permitted to access and download under applicable terms and law.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renxia/skills/m3u8-media-downloader)
- [Upstream CLI repository listed by artifact](https://github.com/lzwme/m3u8-dl)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell commands, TypeScript snippets, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local output files produced by the downloader and requires m3u8dl plus ffmpeg for supported conversion workflows.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
