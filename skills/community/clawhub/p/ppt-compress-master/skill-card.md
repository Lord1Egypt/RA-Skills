## Description: <br>
This skill helps agents compress PowerPoint (.pptx) files by reducing embedded video and large image size, using ffmpeg for video, Pillow for images, and repackaging the result as a valid .pptx. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TsingCode](https://clawhub.ai/user/TsingCode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and productivity-focused agents use this skill to shrink large PowerPoint presentations before sharing, emailing, or archiving them. It is most useful for .pptx files that contain embedded videos or large images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download executable ffmpeg binaries without integrity checks. <br>
Mitigation: Prefer a trusted system ffmpeg package or verify downloaded ffmpeg binaries before use. <br>
Risk: The compression script may install Pillow into the active Python environment. <br>
Mitigation: Run the skill in a virtual environment and install dependencies explicitly before execution. <br>
Risk: Command templates using python -c can be unsafe if built from untrusted filenames or pasted message text. <br>
Mitigation: Validate the .pptx path first and avoid executing commands assembled from untrusted text. <br>
Risk: Video and image compression can reduce media quality or affect playback compatibility. <br>
Mitigation: Keep the original presentation, use dry-run or conservative quality settings for important files, and review the compressed output before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TsingCode/ppt-compress-master) <br>
- [ffmpeg Windows builds](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip) <br>
- [ffmpeg macOS builds](https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip) <br>
- [ffprobe macOS builds](https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip) <br>
- [ffmpeg Linux static builds](https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated .pptx file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a compressed PowerPoint file, typically named with a _compressed suffix, and reports size changes when execution completes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
