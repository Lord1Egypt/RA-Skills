## Description:

Helps agents create and validate Persian documents with right-to-left layout, mixed-direction text, and professional typography.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ehsanghaffar](https://clawhub.ai/user/ehsanghaffar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill to produce and check Persian reports, letters, and technical documents in DOCX, PDF, or Markdown, including content mixed with English text and numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document generation may write to unintended paths or use unexpected configuration.

Mitigation: Review output paths and configuration files before running the scripts.

Risk: PDF generation builds HTML from supplied document text.

Mitigation: Use document content you trust when generating PDFs.

## Reference(s):

- [Persian typography rules](artifact/references/persian-typography.md)
- [Document generation patterns](artifact/references/document-patterns.md)
- [Persian Documents on ClawHub](https://clawhub.ai/ehsanghaffar/skills/persian-documents)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance, Files]

**Output Format:** [Persian text or Markdown, with generated DOCX or PDF files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Right-to-left formatting and mixed Persian/Latin text; rendered documents should be checked for layout and readability.]

## Skill Version(s):

0.1.2 (source: SKILL.md frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
