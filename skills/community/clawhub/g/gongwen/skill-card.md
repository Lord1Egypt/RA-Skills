## Description: <br>
Drafts and reviews Chinese official and administrative documents against GB/T 9704-2012, the 2012 Party and government document handling rules, document-type conventions, format requirements, language patterns, and common-error checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[farmer-data](https://clawhub.ai/user/farmer-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Public-sector staff, administrative writers, and enterprise managers use this skill to select the correct Chinese document type, draft or revise notices, requests, reports, replies, letters, minutes, and summaries, and check format and language conventions. It can also help produce a standards-oriented .docx file from a markdown-style draft. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated official-looking documents may contain incorrect facts, unsuitable wording, or content the user is not authorized to issue. <br>
Mitigation: Review every generated document for factual accuracy, approval authority, and organizational policy before sharing or filing it. <br>
Risk: The optional DOCX renderer reads an input path and writes an output path on the local filesystem. <br>
Mitigation: Run the optional dependency in a virtual environment and choose input and output paths deliberately. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/farmer-data/gongwen) <br>
- [Document Types](artifact/references/document_types.md) <br>
- [Format Standard](artifact/references/format_standard.md) <br>
- [Language Patterns](artifact/references/language_patterns.md) <br>
- [Common Mistakes](artifact/references/common_mistakes.md) <br>
- [DOCX Renderer](artifact/scripts/render_docx.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, files] <br>
**Output Format:** [Markdown or plain-text drafting guidance, with optional DOCX files generated from markdown input.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional DOCX generation requires python-docx and local input and output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
