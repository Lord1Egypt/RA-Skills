## Description: <br>
Packages the MeowMusicServer YouTube fallback workflow for cookie sync, server setup, yt-dlp and ffmpeg audio handling, old-source-first source resolution, and cached MV-to-MP3 extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joe12801](https://clawhub.ai/user/joe12801) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add YouTube fallback audio acquisition to MeowMusicServer or similar music services while preserving legacy sources first. It helps wire cookie sync, server runtime setup, MP3 extraction, cache reuse, and troubleshooting for YouTube download failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow exports and uploads YouTube or Google browser cookies, which should be treated like login credentials. <br>
Mitigation: Use only a server and browser profile you control, prefer a dedicated account, require trusted HTTPS or private-network transport, enforce real admin authorization, restrict file permissions, keep retention short, and rotate or delete cookies when no longer needed. <br>
Risk: The server bootstrap path changes system packages and installs runtime tooling on the target host. <br>
Mitigation: Review the bootstrap script before production use, run it only on an intended Debian or Ubuntu-like host, test in staging first, and verify Node.js, yt-dlp, yt-dlp-ejs, and ffmpeg after installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/joe12801/meowmusic-youtube-mp3) <br>
- [Cookie API and Windows Sync](references/cookie-api-and-sync.md) <br>
- [Known-Good Context](references/known-good-context.md) <br>
- [MeowMusic Integration Notes](references/meowmusic-integration.md) <br>
- [Server Runtime Notes](references/server-runtime-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include server setup steps, patch patterns, and cookie-sync commands that require user review before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
