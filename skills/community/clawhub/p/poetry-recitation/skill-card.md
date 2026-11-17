## Description:

Generate poetry recitation videos using a cloned voice or system voice with a starry background and Chinese subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyanbo2007](https://clawhub.ai/user/zhangyanbo2007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn poem text into a narrated video with timed Chinese subtitles. It is intended for poetry or literary recitation workflows, not background video generation, music generation, or general text-to-speech.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an existing cloned voice automatically for poem recitations without an extra confirmation step.

Mitigation: Review the selected voice and confirm appropriate authorization before generating or sharing recitation videos.

Risk: The skill accepts user-supplied output paths and can write videos outside the expected workspace location.

Mitigation: Use workspace-contained output paths, avoid sensitive directories, and review the final output path before execution.

Risk: Generated videos combine spoken content and subtitles that may be shared beyond the local workspace.

Mitigation: Review poem text, voice choice, and the finished video before distributing it.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Shell commands, Text]

**Output Format:** [MP4 video file with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates 1920x1080, 24 fps H.264/AAC video and writes to the workspace audio directory by default.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
