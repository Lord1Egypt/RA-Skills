## Description:

Use when converting scanned PDFs or documents to markdown/JSON/HTML. Marker (Datalab) uses surya OCR for 90+ languages including Arabic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mina-atef-00](https://clawhub.ai/user/mina-atef-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert scanned PDFs and other documents into markdown, JSON, HTML, or chunks for search, RAG, wiki ingestion, and document analysis workflows. It is especially useful for Arabic or multilingual OCR workflows that need command-line usage, Python API guidance, and post-OCR cleanup steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installer commands can execute code from an external source.

Mitigation: Review installer scripts before running them and install only from sources the user trusts.

Risk: External LLM services may receive document text or images when optional LLM processing is enabled.

Mitigation: Avoid external LLM options for confidential documents unless that data sharing is acceptable; prefer local OCR or a local Ollama setup for sensitive files.

Risk: Large OCR model downloads and OCR workloads can consume significant bandwidth, time, memory, or GPU resources.

Mitigation: Plan for first-run model downloads, reduce worker count when memory is limited, and use local resource settings such as CPU mode when GPU detection is unsuitable.

## Reference(s):

- [Arabic OCR Cleanup](references/arabic-ocr-cleanup.md)
- [Skill homepage](https://github.com/mina-atef-00/agent-skills)
- [Surya OCR](https://github.com/VikParuchuri/surya)
- [ClawHub skill page](https://clawhub.ai/mina-atef-00/skills/marker-pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OCR conversion commands, optional LLM setup, output-format choices, verification checks, and Arabic cleanup guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
