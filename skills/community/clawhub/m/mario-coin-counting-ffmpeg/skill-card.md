## Description: <br>
Extract key frames (I-frames) from video files using FFmpeg command line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-processing users use this skill to generate FFmpeg commands that extract keyframes, thumbnails, or important frames from common video formats for analysis, previews, or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FFmpeg must be installed from a trusted source before users run generated commands. <br>
Mitigation: Confirm the local FFmpeg installation source and version before using the commands. <br>
Risk: Frame extraction can create many files or overwrite files that match the chosen output pattern. <br>
Mitigation: Use a deliberate output directory and filename pattern, and review existing files before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnj22/mario-coin-counting-ffmpeg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces FFmpeg command examples and option guidance for user-selected input videos and output patterns.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
