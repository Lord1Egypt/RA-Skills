## Description: <br>
Universal video downloader supporting multiple platforms (Douyin, Bilibili, YouTube, TikTok, etc.). Can download videos by URL or search by keyword (Douyin supported). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwkGit](https://clawhub.ai/user/wwkGit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to download videos from supported video platforms by URL, batch URL list, or Douyin keyword search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser-backed downloads may use cookies or logged-in session context. <br>
Mitigation: Run the skill in an isolated environment or dedicated browser profile, and do not connect it to personal logged-in browser sessions. <br>
Risk: The skill can download content from third-party video platforms. <br>
Mitigation: Use it only for content the user is permitted to download and review applicable platform terms before use. <br>
Risk: The skill depends on downloader and browser automation packages. <br>
Mitigation: Verify the yt-dlp and DrissionPage dependencies before installation and keep them updated from trusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwkGit/multi-platform-video-downloader) <br>
- [Docker usage guide](DOCKER_README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated video and JSON metadata files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads video files and per-video metadata into user-selected output directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
