## Description:

Helps agents convert documents with Pandoc across Markdown, DOCX, PDF, HTML, EPUB, LaTeX, Typst, RST, AsciiDoc, Org, ODT, RTF, and notebooks, with validation, batch conversion, citations, templates, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwei1125](https://clawhub.ai/user/liuwei1125)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to convert individual documents or batches between common publishing formats while checking dependencies, references, citations, templates, resources, and PDF engines before conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Pandoc option access can run local code through Pandoc filters when untrusted options are accepted.

Mitigation: Review conversion options before execution and avoid accepting --filter, --lua-filter, or other unreviewed Pandoc options from untrusted prompts or files.

Risk: The optional installer can modify the local system when run with --yes.

Mitigation: Run the installer in dry-run mode first and require explicit user approval before executing it with --yes.

## Reference(s):

- [Pandoc Format Reference](references/formats.md)
- [Pandoc Conversion Workflows](references/workflows.md)
- [Pandoc Troubleshooting](references/troubleshooting.md)
- [Pandoc Installing Guide](https://pandoc.org/installing.html)
- [ClawHub Skill Page](https://clawhub.ai/liuwei1125/skills/pandoc-convert-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell commands, conversion status, generated file paths, and optional Markdown or JSON batch reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce converted document files when the agent runs the bundled Pandoc wrappers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
