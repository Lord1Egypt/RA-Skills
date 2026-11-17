## Description:

Converts PDF files into PNG or JPG images locally, with configurable resolution and page ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly3094](https://clawhub.ai/user/fly3094)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to convert local PDF documents into image files for document processing, previews, extraction workflows, or batch conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on Node.js packages for PDF rendering, and dependency resolution may install packages required at runtime.

Mitigation: Install and run it only in environments where npm dependency resolution is acceptable, and verify required packages before deployment.

Risk: The converter may require the canvas package or native canvas dependencies to render pages successfully.

Mitigation: Confirm canvas is installed and operational in the target runtime before relying on the converter in an agent workflow.

Risk: The usage text is primarily in Chinese, which can make setup and troubleshooting harder for non-Chinese users.

Mitigation: Provide translated runbook notes or operator guidance for teams that do not read Chinese.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fly3094/skills/pdf-to-images)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG or JPG image files with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports scale values from 0.5 to 5.0 and optional page ranges such as 1-3,5.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
