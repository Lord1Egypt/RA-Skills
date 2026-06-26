## Description: <br>
Extracts text and tables from PDF files, fills PDF forms, and merges documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RainShow](https://clawhub.ai/user/RainShow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill when they need help extracting PDF text or table data, filling PDF forms, or merging multiple PDF files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF processing can modify or combine user documents, including sensitive PDFs or form data. <br>
Mitigation: Specify exact input files, operations, and output paths; keep original files unchanged until outputs are reviewed. <br>
Risk: Dependency installation may add local packages required for PDF parsing. <br>
Mitigation: Review proposed install commands and run them in the intended environment before processing documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RainShow/pdf-processing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python-oriented implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose dependency installation and file operation steps for user-specified PDFs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
