## Description:

PDF document parsing tool based on local MinerU, supports converting PDF to Markdown, JSON, and other machine-readable formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baokui](https://clawhub.ai/user/baokui)

### License/Terms of Use:


## Use Case:

Developers and document-processing teams use this skill to convert local PDF files into Markdown or structured JSON while preserving document structure, formulas, tables, and images. It is suited for academic papers, technical documents, OCR workflows, multilingual PDFs, and batch document processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation broadly changes Python packages by upgrading pip, installing uv, and installing the full MinerU dependency set.

Mitigation: Install and run the skill only in an isolated virtual environment or container, and review or pin MinerU dependencies before use.

Risk: Output handling can read unrelated files from the selected output directory.

Mitigation: Use a fresh empty output directory for each run, and do not point output_dir at a home, project, or shared directory.

## Reference(s):

- [MinerU Official Documentation](https://opendatalab.github.io/MinerU/)
- [MinerU GitHub](https://github.com/opendatalab/MinerU)
- [MinerU Online Demo](https://mineru.net/)
- [ClawHub Skill Page](https://clawhub.ai/baokui/skills/pdf-parser-mineru)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON status objects with generated Markdown, JSON, image, and document parsing files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written to a user-selected output directory; parsing may take up to one hour per invocation.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
