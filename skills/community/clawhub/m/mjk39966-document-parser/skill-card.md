## Description: <br>
Parse and extract content from .docx, .pdf, and .txt documents, including plain text and tables, so an agent can analyze or answer questions about document contents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjk39966-glitch](https://clawhub.ai/user/mjk39966-glitch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and document-focused agents use this skill to parse local Word, PDF, and text files into extracted text, tables, and metadata for summarization, question answering, and data lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The parser can expose the full contents of local documents in terminal output or agent context. <br>
Mitigation: Use the skill only with deliberately selected files, avoid unnecessary confidential documents, and review extracted output before sharing it further. <br>
Risk: Dependency installation modifies the active Python environment. <br>
Mitigation: Install and run the parser in a virtual environment when possible. <br>
Risk: Scanned PDFs and complex PDF tables may produce incomplete extraction results. <br>
Mitigation: Use source documents with selectable text and verify extracted tables against the original document before relying on them. <br>


## Reference(s): <br>
- [Document Parser Usage Examples](references/usage_examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mjk39966-glitch/mjk39966-document-parser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or human-readable text with extracted document text, tables, and metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on user-selected files; PDF table extraction depends on pdfplumber, and scanned PDFs without selectable text are not supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
