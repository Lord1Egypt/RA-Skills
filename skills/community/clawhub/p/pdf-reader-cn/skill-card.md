## Description: <br>
Extract text, tables, and metadata from PDFs; analyze, summarize, and search PDF content, including specific pages or page ranges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wancy86](https://clawhub.ai/user/wancy86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and document-analysis users can use this skill to extract PDF text, tables, and metadata, inspect page-level content, and generate concise PDF analysis from local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive PDF text or metadata may be printed to terminal output, logs, or shared shell sessions. <br>
Mitigation: Run the scripts only on PDFs you are authorized to inspect, avoid shared terminals for sensitive documents, and redirect or delete output files according to your data-handling policy. <br>
Risk: The scripts read local PDF files provided by the user. <br>
Mitigation: Use trusted PDF inputs and a trusted Python environment when processing private or untrusted documents. <br>


## Reference(s): <br>
- [PDF Python Libraries Reference](references/pdf-libraries.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wancy86/pdf-reader-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON output from the bundled PDF scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included scripts can print extracted PDF text, tables, metadata, page statistics, previews, and JSON-formatted analysis to the terminal.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
