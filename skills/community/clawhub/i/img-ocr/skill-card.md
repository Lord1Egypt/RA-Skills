## Description:

Image text recognition tool based on Tesseract OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ginntech](https://clawhub.ai/user/ginntech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use this skill to extract Chinese and English text from user-selected images and screenshots with local Tesseract OCR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill adds local OCR dependencies, including Tesseract and Python packages.

Mitigation: Install it only when those dependencies are acceptable for the environment, preferably in a virtual environment with pinned package versions.

Risk: OCR should be limited to user-selected image files.

Mitigation: Use the skill only with explicit image paths supplied for OCR and avoid treating it as a general image-analysis tool.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text OCR output and Markdown usage guidance with bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on a user-provided image path and depends on Python, Pillow, pytesseract, Tesseract OCR, and the Chinese language pack.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
