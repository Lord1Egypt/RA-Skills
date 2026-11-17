## Description:

Extract text from images, documents and scanned PDFs using OpenOCR, including text detection, text recognition, universal VLM recognition, and document parsing with layout analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[topdu](https://clawhub.ai/user/topdu)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to extract text, formulas, tables, and structured document content from images, scanned documents, and PDFs. It supports OCR workflows that produce plain text, Markdown, JSON, visualizations, and code or command guidance for OpenOCR usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared Gradio demo commands can expose document-processing interfaces and uploaded content beyond the local machine.

Mitigation: Bind demos to localhost unless remote access is intentional, avoid shared demo links for confidential documents, and run the skill in an isolated environment.

Risk: Generated text, Markdown, JSON, and visualization files may contain sensitive information from source documents.

Mitigation: Classify generated files with the same sensitivity as the original documents and restrict storage, sharing, and retention accordingly.

Risk: Unpinned packages or model artifacts can change behavior between runs.

Mitigation: Use pinned package and model versions and verify artifacts before use.

## Reference(s):

- [OpenOCR GitHub](https://github.com/Topdu/OpenOCR)
- [PyPI Package](https://pypi.org/project/openocr-python/)
- [UniRec Paper](https://github.com/Topdu/OpenOCR#unirec)
- [OpenDoc Documentation](https://github.com/Topdu/OpenOCR#opendoc)
- [Model Zoo and Configs](https://github.com/Topdu/OpenOCR/tree/main/configs)
- [ClawHub Skill Page](https://clawhub.ai/topdu/skills/openocr-skill)
- [Publisher Profile](https://clawhub.ai/user/topdu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; OCR workflows may produce text, JSON, Markdown, LaTeX, or visualization files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may contain sensitive source-document content and should be handled according to the sensitivity of the processed documents.]

## Skill Version(s):

0.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
