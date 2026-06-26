## Description: <br>
Download an Instagram Reel via sssinstagram.com and return it as a WhatsApp-ready video file. Use when a reel URL is provided and yt-dlp is blocked or not preferred. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beSaif](https://clawhub.ai/user/beSaif) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to download a user-provided Instagram Reel through sssinstagram.com and send the resulting local video file through WhatsApp. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Instagram Reel URLs are shared with sssinstagram.com during download. <br>
Mitigation: Use the skill only when sharing the Reel URL with that third-party service is acceptable. <br>
Risk: The skill runs local browser automation using the configured browser binary. <br>
Mitigation: Keep BROWSER_EXECUTABLE_PATH pointed at a trusted Chromium-compatible browser and run the workflow in an appropriate sandbox. <br>
Risk: Downloaded videos are written to the configured download directory. <br>
Mitigation: Set REEL_DOWNLOAD_DIR to a narrow, non-sensitive location and use the cleanup script when retained files are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/beSaif/instagram-reel-downloader-whatsapp) <br>
- [sssinstagram Reels Downloader](https://sssinstagram.com/reels-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and a MEDIA_PATH file result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local video file path for WhatsApp media sending; supported video extensions are mp4, mov, mkv, and webm.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
