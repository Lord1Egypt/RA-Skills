## Description: <br>
Converts Markdown files to Word documents and Word documents to Markdown while preserving common document structure where supported. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangesun](https://clawhub.ai/user/huangesun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to convert individual or multiple Markdown and Word documents between .md and .docx formats and receive the converted output path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests persistent memory access that is not explained by the document conversion workflow. <br>
Mitigation: Review the skill before installing and ask the publisher to remove or clearly justify memory_read and memory_write. <br>
Risk: Generic trigger phrases may cause the skill to activate for broad file or format conversion requests. <br>
Mitigation: Use the skill only for Markdown and Word documents you intend to convert, and confirm the selected input files and output directory before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Converted .docx or .md files with JSON conversion status and concise Markdown-facing guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are written to the configured output directory, defaulting to converted/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
