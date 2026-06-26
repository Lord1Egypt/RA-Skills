## Description: <br>
Split, merge, watermark, and extract text from PDF files - PyPDF2 based. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[martin-sh-ni](https://clawhub.ai/user/martin-sh-ni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing agents use this skill to merge, split, watermark, and extract text from PDF files for workflows such as contract assembly, chapter extraction, and confidential document handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF files and extracted text can contain confidential or sensitive information. <br>
Mitigation: Treat source PDFs and extracted text as sensitive, and avoid sending confidential content to logs or external services unless explicitly intended. <br>
Risk: PDF editing operations can overwrite or alter important documents if output paths are reused carelessly. <br>
Mitigation: Use new output filenames and keep backups for important documents before running merge, split, or watermark operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/martin-sh-ni/pdf-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured parameter guidance and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe PDF operation modes, file path inputs, output filenames, and returned success, text, or message fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
