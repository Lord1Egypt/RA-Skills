## Description:

Generate premium enterprise-style PDFs from markdown content, with automatic de-AI text humanization and a professional Navy + Gold design system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreasozzo](https://clawhub.ai/user/andreasozzo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and document authors use this skill to turn markdown text or markdown files into polished PDF reports, proposals, and business documents. The skill is useful when an agent needs to generate a styled PDF and return the generated file path to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally rewrites markdown text before rendering, which can change wording or meaning in the generated PDF.

Mitigation: Review generated PDFs before sharing or relying on them, especially for legal, financial, medical, or customer-facing documents.

Risk: The skill reads user-supplied markdown files and optional logo image files from paths passed on the command line.

Mitigation: Pass only markdown and logo files the user intended the agent to read, and avoid pointing the skill at unrelated or sensitive files.

Risk: The skill depends on Python packages installed from requirements.txt.

Mitigation: Install dependencies in a virtual environment and avoid package installation with administrator privileges.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andreasozzo/skills/premium-pdf)
- [Publisher Profile](https://clawhub.ai/user/andreasozzo)

## Skill Output:

**Output Type(s):** [files, shell commands, markdown, guidance]

**Output Format:** [PDF file plus terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads markdown text or a markdown file, optionally reads a PNG or JPG logo, writes a PDF to the requested output path, and prints the absolute path of the generated PDF.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
