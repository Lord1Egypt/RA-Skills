## Description:

Provides a structured workflow and script interface for pathology ROI selection tasks in whole slide images.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and pathology data teams can use this skill to structure ROI selection workflows for whole slide images, including AI training data preparation, research sampling, and education. The packaged script currently provides bounded example ROI output rather than validated image analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script returns fixed mock ROI detections rather than performing validated pathology image analysis.

Mitigation: Do not use outputs for medical, research, training-data, or educational ROI decisions until genuine validated image analysis is implemented and synthetic output is clearly labeled.

Risk: The script can write results to any caller-supplied output path.

Mitigation: Validate and restrict output paths to a dedicated workspace directory before execution.

## Reference(s):

- [Pathology ROI Selector on ClawHub](https://clawhub.ai/aipoch-ai/skills/pathology-roi-selector)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with optional shell commands and JSON ROI coordinate output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write ROI coordinate files when an output path is provided]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
