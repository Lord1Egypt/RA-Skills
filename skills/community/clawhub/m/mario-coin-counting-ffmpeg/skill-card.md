## Description:

Extract key frames (I-frames) from video files using FFmpeg command line tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video-processing practitioners use this skill to ask an agent for FFmpeg commands that extract I-frames, thumbnails, or important video frames from common media formats for analysis, previews, or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FFmpeg keyframe extraction may create many image files depending on the source video's encoding and keyframe frequency.

Mitigation: Run commands in a dedicated output directory and review the output pattern before execution.

Risk: The agent may propose FFmpeg commands that operate on user-specified local video files.

Mitigation: Execute commands only against intended input files and review generated shell commands before running them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces FFmpeg command examples and notes; users supply input videos and output patterns.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
