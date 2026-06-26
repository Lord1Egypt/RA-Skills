## Description: <br>
Download the main video from a Pinterest pin and save it as a local MP4 for personal media workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hekaiii](https://clawhub.ai/user/hekaiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to save the primary video from a Pinterest pin as a local MP4 for personal media workflows such as wallpaper saving, repost preparation, or Live Photo conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The downloader uses ffmpeg to fetch remote media and write a local MP4 file. <br>
Mitigation: Use a trusted ffmpeg installation and keep outputs in the stated downloads folder. <br>
Risk: The output file can be overwritten when the chosen path already exists. <br>
Mitigation: Use a disposable or unique output filename and avoid paths that contain important files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hekaiii/pinterest-video-download) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown with local file path and optional MP4 file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves an MP4 under ~/.openclaw/workspace/downloads/ using ffmpeg when a valid HLS playlist is found.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
