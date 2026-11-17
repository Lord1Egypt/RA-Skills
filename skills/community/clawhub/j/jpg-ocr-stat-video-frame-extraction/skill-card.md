## Description:

Extract frames from video files and save them as images using OpenCV

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to extract image frames from video files for video analysis, training dataset creation, thumbnail generation, object detection preprocessing, and image-sequence workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Frame extraction can consume significant disk space for long or high-resolution videos.

Mitigation: Choose a dedicated output folder and confirm adequate free disk space before extraction.

Risk: Reusing an output folder can overwrite or mix frame files with existing outputs.

Mitigation: Use a new output directory or confirm that overwriting same-named frame files is acceptable.

Risk: Some video codecs, damaged files, DRM-protected videos, and variable frame rate videos may fail or produce partial or inaccurate results.

Mitigation: Validate source videos with OpenCV before extraction and report warnings for unsupported codecs, early termination, or seeking issues.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python/OpenCV code examples and JSON result schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for writing image frames to a selected output folder and returning extraction metadata as JSON.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
