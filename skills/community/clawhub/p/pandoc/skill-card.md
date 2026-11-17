## Description:

Convert documents between formats using pandoc, including HTML, Markdown, DOCX, PDF, EPUB, LaTeX, ODT, RST, Org, MediaWiki, JIRA, CSV, and Jupyter notebooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oliver-hrkltz](https://clawhub.ai/user/oliver-hrkltz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill to convert, transform, and export documents across pandoc-supported formats, with options for styling, metadata, table of contents, templates, and PDF engine selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advanced pandoc options such as filters, templates, resource paths, and media extraction can read or execute user-selected local resources through pandoc behavior.

Mitigation: Review source files, output paths, and advanced pandoc flags before conversion; only use filters, templates, resource paths, and media extraction directories that the user intentionally selected.

Risk: Document conversion writes local output files and may overwrite a path chosen by the user or agent.

Mitigation: Confirm the intended output path and directory before running conversion, and keep generated files in an expected workspace location.

## Reference(s):

- [Pandoc Documentation](https://pandoc.org)
- [Pandoc Skill Homepage](https://github.com/hrkltz/pandoc-skill)
- [Pandoc Supported Formats Reference](references/formats.md)
- [Tectonic Typesetting](https://tectonic-typesetting.github.io/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or guide creation of local document output files through pandoc when the agent runs the helper script.]

## Skill Version(s):

1.0.2 (source: release evidence and frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
