## Description:

fpdf2 PDF creation - Unicode-safe alternative to reportlab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mina-atef-00](https://clawhub.ai/user/mina-atef-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create searchable text PDFs with fpdf2 when reportlab is unavailable or a lighter Unicode-aware PDF path is sufficient. It provides setup guidance, Python examples, table patterns, and common fpdf2 pitfalls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install the fpdf2 Python dependency before generating PDFs.

Mitigation: Confirm fpdf2 is acceptable for the target environment before installation, as recommended by the security guidance.

Risk: Generated PDF text may fail for non-Latin-1 characters if only built-in fpdf2 fonts are used.

Mitigation: Register a Unicode-capable TTF font before writing non-ASCII text.

Risk: Table generation can fail when table width exceeds the effective page width or obsolete parameter names are used.

Mitigation: Keep table width within pdf.epw and use current fpdf2 table parameters such as first_row_as_headings.

## Reference(s):

- [fpdf2 Table Patterns Reference](references/fpdf2-table-patterns.md)
- [ClawHub skill page](https://clawhub.ai/mina-atef-00/skills/pdf-creation)
- [Project homepage from metadata](https://github.com/mina-atef-00/agent-skills)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance and examples for installing fpdf2, registering Unicode fonts, creating PDFs, and rendering tables.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
