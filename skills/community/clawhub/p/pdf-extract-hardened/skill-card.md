## Description:

Extract text from PDF files for LLM processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to extract plain text from PDF documents for local review or LLM processing, including optional page-range extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted PDF text may contain sensitive or regulated information that should not be persisted unintentionally.

Mitigation: Return extracted text in the conversation by default and write to a named output file only when the user explicitly requests that destination.

Risk: Extracted PDF text could be sent to network endpoints through pipes, redirects, webhooks, or scripts.

Mitigation: Extract locally and avoid piping or redirecting pdftotext output to network-transmitting commands.

Risk: Internal, confidential, or PII-containing PDF content could be exposed through shared logs, group chats, or build systems.

Mitigation: Match the output location to the content sensitivity and avoid shared channels for sensitive extracted text.

Risk: Installing the required PDF extraction tool may require sudo and trust in OS package repositories.

Mitigation: Confirm the user is comfortable installing poppler-utils from their operating system package repositories before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/pdf-extract-hardened)
- [Faberlens safety evaluation](https://faberlens.ai/explore/pdf-extract)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash command examples and extracted text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local pdftotext binary from poppler-utils.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
