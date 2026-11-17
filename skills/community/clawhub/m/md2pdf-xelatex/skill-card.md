## Description:

Converts Markdown files to PDF with Pandoc and XeLaTeX, including LaTeX math, code blocks, tables, and mixed CJK/Latin text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaruoji](https://clawhub.ai/user/huaruoji)

### License/Terms of Use:


## Use Case:

Developers and other users use this skill to convert trusted Markdown reports, notes, and technical documents into printable PDFs with math and CJK text support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Markdown may include raw TeX that XeLaTeX interprets under the local user's permissions.

Mitigation: Use the skill only with Markdown you created or otherwise trust, or run conversion inside a container or sandbox for downloaded or user-submitted files.

Risk: PDF generation depends on local Pandoc, XeLaTeX, fontconfig, and CJK font availability.

Mitigation: Install the documented TeX and font packages before use, and verify CJK font availability when converting mixed CJK and Latin text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaruoji/skills/md2pdf-xelatex)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PDF file plus Markdown guidance with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local pandoc, xelatex, fontconfig, and suitable fonts; intended for trusted Markdown input.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
