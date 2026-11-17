## Description:

Convert documents between 40+ formats using pandoc CLI, including Markdown, Word, PDF, HTML, LaTeX, and EPUB, with smart defaults, professional templates, and conversion tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thejorgeschmidt](https://clawhub.ai/user/thejorgeschmidt)

### License/Terms of Use:


## Use Case:

Developers, technical writers, and documentation teams use this skill to convert local documents across Pandoc-supported formats, prepare professional PDFs or EPUBs, and generate repeatable conversion commands with validation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch conversions can create or overwrite output files on the local filesystem.

Mitigation: Use an explicit output directory, review target paths before execution, and back up source documents before batch operations.

Risk: The inspected artifact references helper scripts, templates, and documentation that are not included in the artifact.

Mitigation: Confirm required local tooling and files exist before relying on helper-script, template, or extended documentation workflows.

Risk: PDF and EPUB workflows may require external tools such as LaTeX engines, wkhtmltopdf, or epubcheck.

Mitigation: Install and verify optional dependencies before using those output formats, and validate generated files before sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thejorgeschmidt/skills/pandoc-convert-openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local file conversion outputs when Pandoc commands are executed by the user or agent.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
