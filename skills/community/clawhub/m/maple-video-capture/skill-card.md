## Description: <br>
Capture key frames from video files at fixed time intervals for video understanding, screenshot extraction, and frame-level content analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chentx1243](https://clawhub.ai/user/Chentx1243) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to extract representative still images from local videos at fixed intervals, optionally skipping similar frames to reduce redundant screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted frames can expose confidential or sensitive video content because disk output is expected. <br>
Mitigation: Use approved local videos, choose secure output folders, and remove generated images when they are no longer needed. <br>
Risk: Frame extraction creates local image artifacts that may persist after analysis. <br>
Mitigation: Review output locations before running the skill and include generated frames in normal data-retention and cleanup workflows. <br>


## Reference(s): <br>
- [Video Formats Supported](references/video_formats.md) <br>
- [ClawHub skill page](https://clawhub.ai/Chentx1243/maple-video-capture) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with Python command examples and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated frames are saved as JPG or PNG files in the selected output directory with source-video, timestamp, and sequence information in the filename.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
