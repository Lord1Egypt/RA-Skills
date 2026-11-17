## Description:

Translates PPTX files to another language while preserving layout through a LibreOffice render and vision verification loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimo1987](https://clawhub.ai/user/nimo1987)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to translate editable PPTX presentations while preserving layout, then return the translated PPTX and optional render artifacts for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing untrusted presentation files can expose the workflow to unsafe or malformed local PPTX content.

Mitigation: Use trusted PPTX files and review the generated presentation before sharing or relying on it.

Risk: The activation wording mentions PPT/PPTX, but the artifact only supports modern PPTX files.

Mitigation: Do not rely on the skill for legacy .ppt files; convert or reject legacy presentations before use.

Risk: Careless output path selection can place generated files somewhere unintended.

Mitigation: Specify output paths deliberately and inspect the output location after each run.

## Reference(s):

- [PPT Translator ClawHub skill page](https://clawhub.ai/nimo1987/skills/ppt-translator)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Guidance]

**Output Format:** [Editable PPTX files, optional PNG renders, JSON text extraction, and Markdown guidance with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local PPTX input, python-pptx, and LibreOffice; external agent vision is used to verify render overflow.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
