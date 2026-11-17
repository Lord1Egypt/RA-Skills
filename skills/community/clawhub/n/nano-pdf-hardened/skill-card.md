## Description:

Edit PDFs with natural-language instructions using the nano-pdf CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document operators use this skill to apply specific natural-language edits to PDF pages through the nano-pdf CLI while confirming batch scope and sensitive document values before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned third-party nano-pdf CLI package that runs locally on user PDFs.

Mitigation: Install only when the package is trusted for the deployment context, and review sensitive files and outputs before sharing.

Risk: Batch edits can modify unintended PDF files if the resolved file list is not checked first.

Mitigation: List the exact resolved file paths and obtain user confirmation before executing batch edits.

Risk: Sensitive legal, financial, medical, or signed documents can be materially changed by vague instructions.

Mitigation: Confirm the specific fields and replacement values before editing substantive content in sensitive documents.

Risk: Page numbering may differ between zero-based and one-based nano-pdf configurations.

Mitigation: Inspect the output PDF and retry with the alternate page number if the edit lands on the wrong page.

## Reference(s):

- [nano-pdf PyPI package](https://pypi.org/project/nano-pdf/)
- [Nano Pdf Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/skills/nano-pdf-hardened)
- [Faberlens nano-pdf safety report](https://faberlens.ai/explore/nano-pdf)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the nano-pdf CLI and user review of edited PDFs before sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
