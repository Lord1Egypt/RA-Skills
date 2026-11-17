## Description:

Automatically adds relevant academic references to research papers. Supports Overleaf project directories, extracts keywords from TeX files, searches Google Scholar for relevant papers, adds BibTeX entries to the project's bib file, and inserts citation markers in key sections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oldglycine](https://clawhub.ai/user/oldglycine)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and developers use this skill to add academic citations to LaTeX or Overleaf paper projects by extracting topics, finding candidate Google Scholar references, updating BibTeX, and producing an ADD.MD report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change bibliography files using unvalidated remote metadata.

Mitigation: Run it only in a disposable branch or backup copy, inspect proposed references, and verify BibTeX entries before compiling or publishing.

Risk: The documented backup and citation-insertion behavior may overstate what the implementation safely performs.

Mitigation: Do not rely on automated backup or insertion claims unless the implementation is reviewed and fixed for the target paper project.

Risk: Dependency behavior and remote paper lookup may vary at install or runtime.

Mitigation: Pin dependencies in a virtual environment and review the skill carefully before installation.

## Reference(s):

- [Paper Reference Adder Tool](reference/TOOL.MD)
- [ClawHub skill page](https://clawhub.ai/oldglycine/skills/oldglycine-paper-add-citations)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell command examples; generated agent work may update BibTeX and write an ADD.MD report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may propose or perform file changes in a paper project, including bibliography updates and citation report generation.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
