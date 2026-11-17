## Description:

Capture key frames from video files at fixed time intervals, with optional similar-frame skipping to reduce redundant screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chentx1243](https://clawhub.ai/user/chentx1243)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to extract representative still images from local video files for visual review, content recognition, or video summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A hardcoded external dependency path may cause an unexpected Python module to be imported.

Mitigation: Remove the hardcoded D:\SOFTware\py_dependent import path or explicitly control it before running the skill.

Risk: Untrusted videos and unpinned dependencies can increase execution risk on sensitive machines.

Mitigation: Run the skill in an isolated virtual environment and pin and hash dependencies before processing untrusted media.

Risk: Frame files can be overwritten when an output directory already contains files with colliding names.

Mitigation: Use a fresh output directory or confirm that overwriting existing frame files is acceptable.

## Reference(s):

- [Video Formats Supported](references/video_formats.md)
- [ClawHub Skill Page](https://clawhub.ai/chentx1243/skills/maple-video-capture)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [JPEG or PNG image files with terminal log output and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Frames are saved at fixed time intervals with descriptive filenames; similar-frame skipping is optional and configurable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
