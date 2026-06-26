## Description: <br>
Downloads videos or audio from YouTube, Bilibili, Douyin, TikTok, and other supported sites using yt-dlp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chellen021](https://clawhub.ai/user/chellen021) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to download individual videos, audio-only files, subtitles, playlists, or batches of video URLs into a local download directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install or upgrade yt-dlp in the current Python environment during normal use. <br>
Mitigation: Preinstall a trusted, pinned yt-dlp version in an isolated environment before using the skill. <br>
Risk: Downloading playlists or batches can consume substantial local storage and network bandwidth. <br>
Mitigation: Use playlist and batch modes only when the expected storage and network use is intended. <br>
Risk: The skill fetches media from external sites and writes downloaded files locally. <br>
Mitigation: Review the requested URLs and output directory before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chellen021/personal-video-dl) <br>
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; local media files are written by the script when executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output directory is ~/Downloads/Videos; audio-only mode produces MP3 and video mode prefers MP4.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
