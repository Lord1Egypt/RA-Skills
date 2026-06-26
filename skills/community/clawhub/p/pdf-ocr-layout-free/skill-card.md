## Description: <br>
Automates OCR for scanned PDFs by splitting files, submitting chunks to PaddleOCR, and producing layout-preserving searchable PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biabia-55](https://clawhub.ai/user/biabia-55) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing users use this skill when they need an agent to run a repeatable OCR pipeline for scanned PDFs while preserving page layout, headers, footers, and text block placement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs are submitted to an external PaddleOCR API. <br>
Mitigation: Use only documents approved for that provider, review provider terms, and supply a scoped PADDLEOCR_TOKEN. <br>
Risk: Intermediate OCR text, job IDs, chunk PDFs, and merged PDFs are stored in a local work directory. <br>
Mitigation: Choose a controlled work directory and delete it after processing confidential documents. <br>
Risk: The skill installs and runs local Python dependencies and writes output files near the input PDF by default. <br>
Mitigation: Run it in a virtual environment and set explicit --output and --work-dir paths when isolation matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/biabia-55/pdf-ocr-layout-free) <br>
- [PaddleOCR API endpoint used by the pipeline](https://paddleocr.aistudio-app.com/api/v2/ocr/jobs) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and local PDF output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a searchable OCR PDF plus resumable local work-directory artifacts such as chunk PDFs, job IDs, and JSONL OCR results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
