## Description: <br>
Convert PDF files to Markdown with table recognition for extracting text, converting tables, summarizing documents, and fixing formatting issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and document operators use this skill to convert local PDF files into Markdown, plain text, or JSON outputs, including table extraction, header extraction, metadata inspection, and batch conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe filename handling may mishandle untrusted or unusually named PDFs. <br>
Mitigation: Use simple trusted filenames and avoid untrusted PDFs until path handling is fixed. <br>
Risk: Converted text, JSON exports, configuration, and history logs may be retained locally and could contain confidential document content. <br>
Mitigation: Treat the configured data directory as sensitive and delete retained outputs when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/pdf-to-markdown) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [Markdown Syntax Reference](artifact/tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown files, plain text extraction, JSON exports, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally and may retain converted outputs, JSON exports, configuration, and history logs under the configured PDF_TO_MARKDOWN_DIR.] <br>

## Skill Version(s): <br>
3.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
