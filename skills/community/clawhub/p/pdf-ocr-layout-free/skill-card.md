## Description:

Full OCR pipeline for scanned PDFs with layout preservation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biabia-55](https://clawhub.ai/user/biabia-55)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to convert scanned PDFs into searchable, layout-preserving OCR PDFs through a PaddleOCR-based pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF contents are uploaded to the PaddleOCR cloud service for OCR processing.

Mitigation: Use only documents approved for third-party cloud processing, especially when handling confidential, regulated, legal, financial, medical, or proprietary material.

Risk: The skill requires a PADDLEOCR_TOKEN and sends it in API authorization headers.

Mitigation: Provide the token through the environment, avoid hardcoding it in files or prompts, and rotate it if it is exposed.

Risk: The pipeline stores chunk PDFs, job IDs, JSONL OCR results, and chunk OCR PDFs in the work directory for resumability.

Mitigation: Run in an isolated work directory and remove that directory after use when intermediate document copies should not be retained.

Risk: The pipeline fetches service-provided image URLs without destination validation.

Mitigation: Run in a network-restricted or isolated environment when processing sensitive documents, and review outbound access expectations before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biabia-55/skills/pdf-ocr-layout-free)
- [PaddleOCR OCR jobs API endpoint](https://paddleocr.aistudio-app.com/api/v2/ocr/jobs)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration instructions]

**Output Format:** [Markdown instructions with bash commands and generated PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a searchable layout-preserving OCR PDF and a resumable work directory containing chunk PDFs, job IDs, and OCR result files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
