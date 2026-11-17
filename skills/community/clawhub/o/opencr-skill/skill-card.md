## Description:

Extract text from images, documents and scanned PDFs using OpenOCR - supports text detection, recognition, universal VLM recognition, and document parsing with layout analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[topdu](https://clawhub.ai/user/topdu)

### License/Terms of Use:


## Use Case:

Developers and document-processing users use this skill to extract text, formulas, tables, and page structure from images, scanned documents, and PDFs with OpenOCR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public Gradio share links can expose document-processing demos without clear access controls.

Mitigation: Keep demos local or behind authenticated access controls, and do not process confidential documents through public share links.

Risk: OCR and document parsing workflows may save extracted document contents to local output directories.

Mitigation: Choose output directories intentionally, restrict access to them, and remove generated files when they are no longer needed.

Risk: Package and model versions can affect OCR behavior, performance, and reproducibility.

Mitigation: Run the skill in an isolated environment and pin package and model versions where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/topdu/skills/opencr-skill)
- [OpenOCR GitHub](https://github.com/Topdu/OpenOCR)
- [OpenOCR PyPI Package](https://pypi.org/project/openocr-python/)
- [UniRec Documentation](https://github.com/Topdu/OpenOCR#unirec)
- [OpenDoc Documentation](https://github.com/Topdu/OpenOCR#opendoc)
- [Model Zoo and Configs](https://github.com/Topdu/OpenOCR/tree/main/configs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide generation of OCR text, LaTeX, tables, Markdown, JSON, and local output files through OpenOCR workflows.]

## Skill Version(s):

0.1.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
