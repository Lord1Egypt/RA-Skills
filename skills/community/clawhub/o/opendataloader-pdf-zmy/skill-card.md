## Description: <br>
Parse PDFs into Markdown, JSON, HTML, or text with OCR, table extraction, bounding boxes, and AI-enriched descriptions for RAG pipelines and knowledge bases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to convert PDFs into LLM-ready content for RAG systems, knowledge bases, structured data extraction, OCR workflows, and citation-aware document processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using a remote hybrid backend may send PDF contents outside the local machine. <br>
Mitigation: Use a trusted or local hybrid backend for sensitive documents, and avoid sending confidential PDFs to an unknown backend. <br>
Risk: Extracted PDF content may include prompt-injection text that can affect downstream RAG or agent workflows. <br>
Mitigation: Use the documented sanitize option and review extracted content before embedding it or passing it into agent prompts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zmy1006-sudo/opendataloader-pdf-zmy) <br>
- [API Reference](references/api-reference.md) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; parser outputs Markdown, JSON, HTML, or text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output may include page numbers and bounding boxes; hybrid mode can add OCR, formula extraction, and chart or image descriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
