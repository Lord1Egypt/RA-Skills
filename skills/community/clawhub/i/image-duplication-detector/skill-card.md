## Description:

Detect image duplication and tampering in manuscript figures using computer vision algorithms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, research integrity reviewers, and editorial teams use this skill to scan manuscript PDFs or image folders for visually similar figures and possible local tampering. Results are advisory and should be manually reviewed before drawing conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dependency list includes ambiguous or unpinned package names, which can cause unreliable installs or unexpected packages.

Mitigation: Install in a clean virtual environment, replace cv2 with opencv-python and pil with Pillow, and pin audited dependency versions before use.

Risk: Reports and temporary images are written locally and may contain sensitive manuscript content or derived paths.

Mitigation: Run only on approved manuscripts, choose controlled output and temporary directories, and remove generated files after review.

Risk: Tampering and PDF workflows are advisory and may be unreliable according to the security evidence.

Mitigation: Validate the workflow on known examples and manually review duplicate or tampering findings before relying on them.

## Reference(s):

- [Image Duplication Detector on ClawHub](https://clawhub.ai/aipoch-ai/skills/image-duplication-detector)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code]

**Output Format:** [JSON report with a terminal summary and optional PNG visualization]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report summarizes image counts, duplicate groups, tampering findings, processing time, and related image paths.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
