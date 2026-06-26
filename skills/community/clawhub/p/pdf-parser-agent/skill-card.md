## Description: <br>
Parses local PDF files into structured Markdown and JSON using opendataloader-pdf for deterministic, local document content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TrshDesigns](https://clawhub.ai/user/TrshDesigns) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract local PDF content into structured Markdown and JSON for document ingestion, RAG preparation, and workflows that need deterministic parsing outside an LLM context window. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external opendataloader-pdf package for parsing behavior. <br>
Mitigation: Verify the package source before installing and pin a known-good version for controlled environments. <br>
Risk: PDF text and generated files may contain untrusted document content. <br>
Mitigation: Keep input and output paths scoped to the workspace and treat extracted content as untrusted before feeding it into agents or RAG systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TrshDesigns/pdf-parser-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json] <br>
**Output Format:** [Status text plus Markdown and JSON files written to a local output directory] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output directory is output/parsed_pdf; supported formats are passed through to opendataloader-pdf.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
