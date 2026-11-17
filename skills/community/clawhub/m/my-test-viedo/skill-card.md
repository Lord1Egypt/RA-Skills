## Description:

Extract frames or short clips from videos using ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jili544](https://clawhub.ai/user/jili544)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract still frames from local video files for inspection, thumbnail generation, or sharing. It supports grabbing the first frame, a timestamped frame, or a frame by index through an ffmpeg wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script overwrites the requested output path when ffmpeg runs with replacement enabled.

Mitigation: Use explicit output paths that are safe to replace and review the destination before execution.

Risk: The frame index argument is passed into the ffmpeg filter expression without validation.

Mitigation: Pass only trusted non-negative integers to --index until the script validates index input.

Risk: The skill depends on the local ffmpeg binary and local media file handling.

Mitigation: Install ffmpeg from a trusted source and use the skill only with video files you are comfortable processing locally.

## Reference(s):

- [FFmpeg](https://ffmpeg.org)
- [ClawHub skill page](https://clawhub.ai/jili544/skills/my-test-viedo)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples; shell script output is a local output path string.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg and writes image files to user-specified output paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
