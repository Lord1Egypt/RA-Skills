## Description:

Helps Codex work with Microsoft Word (.docx) and WPS Office documents for creation, editing, conversion, text and metadata extraction, analysis, troubleshooting, and batch processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiyunrei2025](https://clawhub.ai/user/baiyunrei2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-automation users can use this skill to generate, edit, inspect, convert, repair, and batch process Office documents while preserving content and formatting where possible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Office document operations can overwrite, corrupt, or unexpectedly change important files.

Mitigation: Use the skill on copies or backups of source documents and validate output in the target Office application.

Risk: Untrusted Office documents may contain unsafe content or trigger risky tooling behavior during extraction or conversion.

Mitigation: Process untrusted documents in a constrained environment and review proposed commands before execution.

Risk: The package references helper files and scripts that are not included in the artifact.

Mitigation: Treat missing referenced helpers as unavailable and rely only on packaged guidance or locally verified tools.

## Reference(s):

- [Text Extraction from Office Documents](references/TEXT_EXTRACTION.md)
- [ClawHub Office Docs Skill Page](https://clawhub.ai/baiyunrei2025/skills/office-docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file edits or generated Office document workflows; users should run document operations on copies of important files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
