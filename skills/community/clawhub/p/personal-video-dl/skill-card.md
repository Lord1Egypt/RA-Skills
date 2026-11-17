## Description:

Downloads videos or audio from YouTube, Bilibili, Douyin, TikTok, and other supported sites using yt-dlp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chellen021](https://clawhub.ai/user/chellen021)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to run a local video downloader for single videos, audio-only downloads, subtitles, playlists, and URL-list batch downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically install or upgrade an unpinned external dependency on the user's machine.

Mitigation: Preinstall a reviewed, pinned yt-dlp version and disable or avoid the automatic installation path before deployment.

Risk: The skill contacts external video services and writes downloaded media files locally.

Mitigation: Run it only for authorized URLs in a controlled download directory with normal review before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chellen021/skills/personal-video-dl)
- [Publisher profile](https://clawhub.ai/user/chellen021)
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download local media files, subtitles, and extracted MP3 audio through yt-dlp.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
