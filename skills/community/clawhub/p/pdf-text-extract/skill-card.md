## Description: <br>
Extracts readable text from local PDF files with PyPDF2 for command-line processing, summarization, or archiving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to extract plain text from local PDFs for downstream processing, summarization, or archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted text may contain sensitive content from the source PDF. <br>
Mitigation: Treat generated text with the same sensitivity as the original PDF and choose output paths carefully. <br>
Risk: The README examples use pdf_text_extract.py while the packaged artifact provides tool.py. <br>
Mitigation: Run the packaged script as tool.py unless it is intentionally renamed. <br>
Risk: Complex, scanned, or image-only PDFs may produce incomplete or poorly ordered text because the tool relies on PyPDF2 extraction. <br>
Mitigation: Review extracted text before downstream use and use an OCR workflow for image-only PDFs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text printed to stdout or written as a UTF-8 text file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local PDF path and a Python environment with PyPDF2 available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
