## Description:

Create real DOCX documents with headings, paragraphs, bullets and tables, and inspect document text structure. Use for Word Document Composer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and developers can create Word documents from supplied material and inspect a DOCX's paragraph and table structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inspection reports contain extracted document text that may be confidential.

Mitigation: Protect or delete exports when handling confidential documents.

Risk: The skill retains a local database in .mochilab/docx-composer.

Mitigation: Keep the host sandbox enabled.

Risk: Generated DOCX layout is not visually verified by the skill.

Mitigation: Check generated documents in Word, LibreOffice, or another available renderer.

## Reference(s):

- [Action contract](references/input.md)
- [MochiLab](https://mochilab.bz)
- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-docx-composer)

## Skill Output:

**Output Type(s):** [Files, Analysis]

**Output Format:** [DOCX documents; JSON and HTML inspection reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates new files under exports/; inspection reports include paragraph text, table count, and source hash. Generated layout is not visually rendered.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
