## Description:

Professional document editing assistant for project proposals, feasibility studies, initiation reports, and similar Chinese-language professional documents that need data edits, logic adjustments, content changes, multi-color highlights, and linked-consistency checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rhymekkhuang](https://clawhub.ai/user/rhymekkhuang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and document editors use this skill to revise Chinese professional proposal-style documents while tracking changed content, checking linked data and references, and producing a concise completion report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Edited proposal documents can lose formatting, omit requested highlights, or leave linked figures, references, and conclusions inconsistent.

Mitigation: Keep an original copy before editing and review the generated DOCX output against the skill's checklist for highlights, data consistency, logic links, formatting, and omissions.

Risk: Installing document-editing dependencies from an untrusted source can introduce dependency-hygiene risk.

Mitigation: Install python-docx only in a trusted virtual environment or from an approved pinned dependency source.

## Reference(s):

- [Proposal Editor Skill Page](https://clawhub.ai/rhymekkhuang/skills/proposal-editor)
- [Publisher Profile](https://clawhub.ai/user/rhymekkhuang)
- [workflows/main.md](artifact/workflows/main.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell commands and document-editing code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce edited document files when paired with document tools such as pandoc, python-docx, or direct DOCX XML editing.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
