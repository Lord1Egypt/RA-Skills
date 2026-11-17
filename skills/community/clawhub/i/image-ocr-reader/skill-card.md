## Description:

Extracts text from image files with Tesseract OCR, supporting Chinese and English recognition for common formats such as JPG, PNG, and JPEG.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igetmm](https://clawhub.ai/user/igetmm)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to run local OCR on user-selected images and return extracted text or structured OCR details for downstream reading, indexing, or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing OCR dependencies from untrusted sources can introduce supply-chain risk.

Mitigation: Install Tesseract, pytesseract, and Pillow from trusted sources in a virtual environment, and pin dependency versions where practical.

Risk: The optional output path writes extracted text to disk and could overwrite or expose data if chosen carelessly.

Mitigation: Use an explicit, intended output path and review where OCR results are saved.

Risk: OCR results can be incomplete or inaccurate, especially for low-quality images or unsupported language packs.

Mitigation: Review extracted text before using it for decisions, records, or downstream automation.

## Reference(s):

- [Image OCR Reader ClawHub listing](https://clawhub.ai/igetmm/skills/image-ocr-reader)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON OCR results, with Markdown guidance and inline shell or Python examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally write extracted text to a user-selected output path; detailed mode returns OCR confidence and bounding box data.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
