## Description: <br>
Convert Microsoft Office documents (DOCX, XLSX, PPTX) to Markdown without any external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to convert DOCX, XLSX, and PPTX files into Markdown for review, indexing, summarization, or downstream LLM processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted Markdown can contain sensitive or untrusted content extracted from user-selected Office documents. <br>
Mitigation: Review generated Markdown before sharing it or feeding it into another agent or workflow. <br>
Risk: Default output paths can create or replace .md files near the selected input or in an output directory. <br>
Mitigation: Use explicit output paths when converting sensitive files and check for existing Markdown files before batch conversion. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, files, shell commands, guidance] <br>
**Output Format:** [Markdown files generated from local Office documents, plus CLI status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-file conversion and batch directory conversion for .docx, .xlsx, and .pptx inputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
