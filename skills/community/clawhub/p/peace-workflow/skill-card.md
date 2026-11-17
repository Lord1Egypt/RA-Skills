## Description:

Peace Workflow automates review, iterative code improvement, versioned output generation, and result delivery for HTML game files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuxnd](https://clawhub.ai/user/kukuxnd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send a selected HTML file for review, apply jury feedback, and produce an improved versioned HTML file with a changelog.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends the selected HTML file and generated result through Feishu, which may expose sensitive or private project content.

Mitigation: Confirm the file path and Feishu target before running the skill, and avoid using it on files that contain confidential data unless sharing is approved.

Risk: The workflow creates new versioned HTML files, so an incorrect target filename can overwrite or misplace expected outputs.

Mitigation: Review the requested input path and next version filename before execution, and keep existing versions available for comparison.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks and generated or modified HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates versioned HTML outputs and includes changelog-style review notes when the workflow is executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
