## Description:

Convert Markdown files to PDF using Pandoc and LaTeX with options for syntax highlighting, table of contents, and custom CSS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangmanqi2104201431-ship-it](https://clawhub.ai/user/yangmanqi2104201431-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to convert trusted Markdown documents into PDFs, including documents that need a table of contents, syntax highlighting, custom CSS, or CJK font support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Markdown processed through Pandoc and LaTeX may expose local files in generated PDFs when hostile raw TeX is present.

Mitigation: Convert only trusted Markdown, or run conversion in a sandbox with access limited to the required input and output directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangmanqi2104201431-ship-it/skills/pdfmd)
- [Pandoc installation documentation](https://pandoc.org/installing.html)
- [MiKTeX download](https://miktex.org/download)
- [LaTeX project](https://www.latex-project.org/get/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown guidance with shell commands and a generated PDF file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Pandoc and a LaTeX engine such as XeLaTeX, LuaLaTeX, or PDFLaTeX.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
