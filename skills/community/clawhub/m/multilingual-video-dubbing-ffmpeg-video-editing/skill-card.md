## Description: <br>
Cut, trim, concatenate, and split video files - basic video editing operations <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video editors use this skill to ask an agent for FFmpeg commands that cut, trim, concatenate, split, or extract segments from local video files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated FFmpeg commands can overwrite or damage valuable video files if paths, timestamps, or output names are wrong. <br>
Mitigation: Review commands before running them, confirm input and output paths, and keep backups of original videos. <br>
Risk: Trim and concatenation commands can produce imprecise cuts or incompatible outputs when stream copying across keyframes or mismatched codecs. <br>
Mitigation: Use re-encoding when precision or codec compatibility matters, and validate the output before replacing source media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnj22/multilingual-video-dubbing-ffmpeg-video-editing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require review before execution and local paths should be confirmed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
