## Description:

Convert Markdown files to beautifully formatted PDFs using Pandoc and Typst, with support for headings, tables, code blocks, links, emojis, and GitHub-style formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hansschinkenwurst78-dev](https://clawhub.ai/user/hansschinkenwurst78-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to convert local Markdown documents into formatted PDFs through a Pandoc and Typst shell workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command uses an unpinned npx path.

Mitigation: Install only after reviewing the resolved package and version, or pin the installer version in controlled environments.

Risk: The converter writes output and temporary files in the source Markdown directory and may overwrite same-named files.

Mitigation: Run conversion in a trusted working directory and check for existing PDF or temporary Typst filenames before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hansschinkenwurst78-dev/skills/openclaw-md2pdf)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PDF file with terminal status text and Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the PDF next to the source Markdown file and uses same-directory temporary Typst files during conversion.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
