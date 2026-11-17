## Description:

Read DOCX and text, search across files and export extracted text and line-cited evidence. Use for Document Reading and Questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

People using an AI assistant can read DOCX and text documents, search across files, and gather source-located answers. They can also export extracted text and line-cited evidence for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents may be shared with the configured AI provider.

Mitigation: Use only documents approved for sharing with that provider.

Risk: Exported passages remain in the workspace until removed.

Mitigation: Review export locations and remove files when they are no longer needed.

## Reference(s):

- [Document Reading and Questions input contract](references/input.md)
- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-document-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Plain text, Markdown, and JSON with source paths, line references, and SHA256 receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [DOCX citations refer to extracted text lines rather than page numbers.]

## Skill Version(s):

1.1.1 (source: evidence.json release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
