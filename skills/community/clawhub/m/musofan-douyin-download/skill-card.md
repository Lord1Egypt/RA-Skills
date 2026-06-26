## Description: <br>
Download Douyin (Chinese TikTok) videos to local MP4 files when a user shares a Douyin or TikTok URL, using exported browser cookies and a trusted local HTTP proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[musofan](https://clawhub.ai/user/musofan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to save Douyin or TikTok videos as local MP4 files from shared video URLs. It is intended for workflows where the user can provide fresh exported site cookies and run a trusted local HTTP proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses exported Douyin or TikTok cookies, which can expose authenticated session data if mishandled. <br>
Mitigation: Keep the cookie file private, store it only locally, refresh it only when needed, and delete it when the download task is complete. <br>
Risk: The download flow sends browser and media traffic through the fixed local proxy at 127.0.0.1:7897. <br>
Mitigation: Run the skill only when that address is controlled by a trusted local proxy configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/musofan/musofan-douyin-download) <br>
- [Publisher profile](https://clawhub.ai/user/musofan) <br>
- [Project homepage](https://github.com/musofan/douyin-download) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Local MP4 file with terminal progress and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads to a user-selected path or sessions/video-download/video.mp4 by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
