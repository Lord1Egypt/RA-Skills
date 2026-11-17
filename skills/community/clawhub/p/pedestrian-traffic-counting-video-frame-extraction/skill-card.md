## Description:

Extract frames from video files and save them as images using OpenCV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to extract image frames from video files for video analysis, machine learning datasets, thumbnail generation, object detection preprocessing, tracking workflows, and sampled image sequences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long or high-resolution videos can create many image files and consume substantial disk space.

Mitigation: Use a controlled output folder and choose intervals or frame ranges before processing large videos.

Risk: Unsupported codecs, encrypted media, or damaged videos can fail to open or produce partial extraction results.

Mitigation: Validate that OpenCV can open the video, inspect metadata before extraction, and return warnings when reads fail early.

Risk: Frame seeking may be inaccurate for some variable-frame-rate videos or container formats.

Mitigation: Verify sampled frames against the source video and use time-based extraction when frame-index seeking is unreliable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lnj22/skills/pedestrian-traffic-counting-video-frame-extraction)
- [Publisher profile](https://clawhub.ai/user/lnj22)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with Python code examples and a JSON result schema]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides OpenCV-based extraction of image files from user-provided videos, including interval, frame range, output format, metadata, warnings, and output file lists.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact Version History lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
