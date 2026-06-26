## Description: <br>
Extract Chinese and English text from images and scanned PDFs, including documents like invoices and contracts, using PaddleOCR in Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roamer-remote](https://clawhub.ai/user/roamer-remote) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-processing users use this skill to extract text from scanned PDFs, images, invoices, contracts, and multi-page documents. It supports Chinese and English OCR workflows through PaddleOCR and an optional local Python script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation may pull packages from untrusted or unintended sources. <br>
Mitigation: Install PaddleOCR dependencies in a virtual environment from trusted package indexes. <br>
Risk: Confidential PDF page images may briefly be written under /tmp and could remain if processing fails. <br>
Mitigation: Process only documents intended for OCR, avoid elevated privileges, and remove temporary files after failed runs. <br>
Risk: A chosen output path could overwrite an existing local file. <br>
Mitigation: Review the output path before running the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roamer-remote/ocr-python) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; script output is recognized text with optional newline-delimited text file output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OCR results include recognized text and confidence scores when using PaddleOCR directly; the bundled script prints recognized text or writes it to a chosen output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
