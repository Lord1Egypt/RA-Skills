## Description: <br>
Extract frames or short clips from videos using ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jili544](https://clawhub.ai/user/jili544) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content reviewers use this skill to extract a first frame, a frame at a timestamp, or an indexed frame from local video files with ffmpeg for inspection or thumbnail creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper writes to user-selected output paths and may overwrite an existing file. <br>
Mitigation: Use a dedicated output directory and review the --out path before running the command. <br>
Risk: Frame extraction depends on the local ffmpeg binary. <br>
Mitigation: Install ffmpeg from a trusted package manager or verified source before using the skill. <br>


## Reference(s): <br>
- [FFmpeg](https://ffmpeg.org) <br>
- [ClawHub skill page](https://clawhub.ai/jili544/my-test-viedo) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and generated image files from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and a local video file.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
