## Description:

Multi-business knowledge base with image attachment and OCR support for managing Q&A databases by business type, auto page splitting, and intelligent search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwl52](https://clawhub.ai/user/wwl52)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, and operations teams use this skill to create and query local business-specific Q&A knowledge bases, attach screenshots, extract OCR text, track unanswered questions, view statistics, and export Markdown documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File handling can escape intended knowledge-base folders and delete or overwrite user-writable files.

Mitigation: Review commands before execution, run the skill in a contained workspace or sandbox, and avoid delete or export commands with untrusted business names, filenames, or output paths.

Risk: Screenshots and OCR text may contain sensitive business or personal information.

Mitigation: Redact sensitive screenshots before attaching them and document local privacy, retention, and cleanup practices for stored images and extracted text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwl52/skills/knowledge-base-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/wwl52)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-style command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create and update local JSON knowledge-base files, copy image attachments, run optional OCR, and export Markdown.]

## Skill Version(s):

2.1.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
