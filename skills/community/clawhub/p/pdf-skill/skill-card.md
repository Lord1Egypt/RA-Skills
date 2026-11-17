## Description:

Create, read, edit, merge, split PDF files. Supports text extraction, table extraction, form filling, watermarks, OCR, and HTML-to-PDF conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weaglewang](https://clawhub.ai/user/weaglewang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing agents use this skill to install PDF tooling and generate, inspect, transform, extract data from, and secure PDF files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF-writing examples can overwrite or create files in the current working directory if paths are left unchanged.

Mitigation: Use explicit safe input and output filenames, and run examples in a working directory that does not contain important PDFs.

Risk: HTML-to-PDF examples can include untrusted data in generated HTML.

Mitigation: Escape or validate untrusted data before passing it into HTML-based PDF generation.

Risk: Optional PDF, OCR, and conversion packages expand the local dependency footprint.

Mitigation: Install only the packages needed for the intended workflow in a virtual environment with reviewed pinned versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weaglewang/skills/pdf-skill)
- [Publisher profile](https://clawhub.ai/user/weaglewang)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces PDF processing instructions and examples for local files; users choose paths, packages, and optional OCR or conversion tools.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
