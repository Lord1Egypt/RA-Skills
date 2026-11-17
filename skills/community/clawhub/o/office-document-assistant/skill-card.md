## Description:

Office Document Assistant helps agents read, extract, summarize, and compare PDF, Word, Excel, and PowerPoint documents using deterministic text extraction with OCR fallback for PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windrunner20](https://clawhub.ai/user/windrunner20)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to extract text from office documents and turn the results into summaries, key points, structured fields, page or slide outlines, and multi-document comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied documents may contain sensitive information and the skill reads the document paths provided to the agent.

Mitigation: Use the skill only on files the user is comfortable giving to the agent, and avoid exposing extracted content beyond the intended session or workflow.

Risk: Text-first extraction and OCR can be incomplete or noisy for scanned PDFs, legacy Office files, charts, and complex layouts.

Mitigation: Preserve extraction warnings, distinguish directly extracted content from summaries or inference, and verify important facts against the source document.

Risk: The skill may invoke local OCR or conversion tools on supplied documents.

Mitigation: Confirm the file path and required dependencies before running extraction, and review generated text before relying on downstream summaries or comparisons.

## Reference(s):

- [Capabilities and Boundaries](references/capabilities.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional JSON extraction output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted document text, summaries, key fields, warnings, and truncation notes.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
