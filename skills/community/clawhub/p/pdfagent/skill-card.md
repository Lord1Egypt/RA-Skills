## Description:

Self-hosted PDF operations and conversions with metered usage output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cap-txt](https://clawhub.ai/user/cap-txt)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to run local PDF workflows such as merge, split, compression, conversion, OCR, redaction, signing, and multi-step agent instructions while receiving usage metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some features can fetch remote URLs for HTML-to-PDF conversion.

Mitigation: Prefer local file inputs and fetch only trusted URLs in environments where network access is allowed.

Risk: Translation and agent planning can send document text to an LLM command or provider.

Mitigation: Avoid --llm-cmd and translation on confidential documents unless the command or provider is trusted for that data.

Risk: PDF passwords may appear in process details or error context when passed on the command line.

Mitigation: Avoid reusable passwords and run the tool on trusted single-user hosts when encrypted PDFs are required.

Risk: Rasterized redaction creates intermediate files during processing.

Mitigation: Clean intermediate files securely and review redacted output before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cap-txt/skills/pdfagent)
- [Publisher profile](https://clawhub.ai/user/cap-txt)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; tool execution can emit JSON usage summaries and PDF, image, text, or office-document files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Machine-readable output is available with --json and includes usage and output file paths.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
