## Description: <br>
Processes PDFs by extracting text, recognizing tables, merging documents, splitting pages, and reading metadata with a pure Python implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and document-heavy teams use this skill to extract PDF text and metadata, merge reports, split documents into pages, and process batches of local PDF files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local PDFs selected by the user and may handle sensitive document content. <br>
Mitigation: Use it only on PDFs approved for agent processing, and avoid highly sensitive files unless the workflow has appropriate access controls. <br>
Risk: The skill can create merged or split output files on disk. <br>
Mitigation: Review output paths before execution and keep generated PDFs in an approved working directory. <br>
Risk: The skill may keep a local pdf_jobs.json log containing job metadata and short text previews. <br>
Mitigation: Remove or disable the log for sensitive workflows, or periodically delete it after processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-pdf-processor) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python code examples and structured result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local merged or split PDF files and a pdf_jobs.json log with job metadata and short text previews.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter, hub.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
