## Description: <br>
Extract structured data from construction PDFs, including specifications, bills of materials, schedules, and reports, into Excel, CSV, or JSON using native PDF parsing or OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, data engineers, and construction project teams use this skill to extract tables, text, schedules, BOM items, and specification sections from construction PDFs into structured files for analysis and downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Construction PDFs and exported structured files may contain sensitive project, commercial, or personal information. <br>
Mitigation: Read only approved PDFs, write outputs to approved local locations, and review exported files before sharing. <br>
Risk: OCR and PDF table extraction can produce low-confidence or malformed structured data. <br>
Mitigation: Review confidence notes, warnings, and page references before relying on extracted data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/pdf-to-structured) <br>
- [Data-Driven Construction](https://datadrivenconstruction.io) <br>
- [pdfplumber documentation](https://github.com/jsvine/pdfplumber) <br>
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code blocks; extracted data may be saved as Excel, CSV, JSON, JSONL, or text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include confidence notes, warnings for low-quality extraction, and original PDF page references.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact/claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
