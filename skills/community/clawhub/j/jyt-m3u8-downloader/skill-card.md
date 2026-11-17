## Description:

Downloads M3U8/HLS video streams by parsing playlists, downloading TS segments concurrently, handling AES-128 keys, and merging segments into MP4 files with ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jyt2018](https://clawhub.ai/user/jyt2018)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve videos from user-provided M3U8/HLS playlist URLs, including nested playlists and encrypted streams when a key is available. It supports preparing the Python environment, invoking the downloader, and producing an MP4 output through ffmpeg.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary reports unsafe network and file handling in the downloader code.

Mitigation: Install only after reviewing or fixing the downloader, and use it with trusted M3U8 URLs in a sandbox with limited network and filesystem access.

Risk: Downloader behavior may write media and temporary files to user-selected paths.

Mitigation: Avoid sensitive output paths and verify the destination before execution.

Risk: The security guidance calls out TLS bypasses and URL/path validation gaps.

Mitigation: Remove TLS bypasses and add URL and path validation before routine use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jyt2018/skills/jyt-m3u8-downloader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When the bundled downloader is executed, it can create local MP4 files plus temporary TS segments, key files, and M3U8 playlists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
