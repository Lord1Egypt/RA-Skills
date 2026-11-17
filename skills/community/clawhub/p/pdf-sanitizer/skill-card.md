## Description:

Detects sensitive information patterns associated with PDFs, including ID numbers, phone numbers, addresses, and bank cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams can use this skill as a PII-detection helper for text extracted from PDF workflows, especially for Chinese ID numbers, phone numbers, bank cards, email addresses, passport numbers, and IP addresses. Review is required before use on real documents because the security evidence says the included script scans text and prints matches rather than completing PDF redaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is described as a PDF redaction tool, but the authoritative security summary says the included script only scans text and prints sensitive matches.

Mitigation: Treat the artifact as a detection helper until PDF parsing, irreversible redaction, output generation, and documentation are verified.

Risk: Sensitive values may be copied into terminal output, saved JSON, logs, or agent transcripts.

Mitigation: Use only test data or controlled environments unless matches are masked by default and output handling is reviewed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/harrylabsj/skills/pdf-sanitizer)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON scan results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included detection script reads text from standard input and emits JSON matches that may contain full sensitive values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
