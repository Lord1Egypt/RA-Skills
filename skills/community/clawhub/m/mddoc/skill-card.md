## Description:

Converts Markdown files or pasted Markdown text into academically formatted Word (.docx) documents with structured headings, body text, tables, images, lists, and LaTeX-style math.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trisia](https://clawhub.ai/user/trisia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, and document authors use mddoc to convert Markdown content into Word documents that follow strict academic formatting for papers, technical reports, and theses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup workflow may create a cached Python environment and download dependencies.

Mitigation: Install in a controlled environment and review dependency setup before running the skill.

Risk: Markdown image references may contact remote or internal URLs or embed local image files into the generated document.

Mitigation: Use trusted Markdown input, or sandbox conversion and disable remote or local image resolution before processing untrusted content.

## Reference(s):

- [mddoc ClawHub listing](https://clawhub.ai/trisia/skills/mddoc)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [DOCX files, with Markdown guidance and shell command invocations for setup and conversion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a cached Python environment when dependencies are missing; generated documents may embed downloaded or local images referenced by Markdown input.]

## Skill Version(s):

0.1.10 (source: ClawHub release evidence; artifact frontmatter reports 1.0.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
