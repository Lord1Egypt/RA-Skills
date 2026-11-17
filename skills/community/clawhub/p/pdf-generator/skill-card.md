## Description:

Generate professional PDFs from Markdown, HTML, data, or code for reports, invoices, contracts, and documents with best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to choose PDF-generation tools and produce implementation patterns for reports, invoices, contracts, forms, and batch document workflows from Markdown, HTML, data, or code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample PDF-output paths could overwrite important files or write to unintended locations when copied into real applications.

Mitigation: Write outputs only to user-chosen directories, validate destination paths, sanitize filenames, and check before overwriting existing files.

Risk: HTML templating examples can be unsafe when populated with untrusted user data.

Mitigation: Escape untrusted data, use a safe templating library, and review generated HTML before PDF conversion.

Risk: PDF rendering tools such as WeasyPrint may fetch local or remote resources if inputs are not restricted.

Mitigation: Restrict resource fetching and only render trusted or pre-sanitized HTML and assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/pdf-generator)
- [Skill homepage](https://clawic.com/skills/pdf-generator)
- [PDF Tools - Selection Guide](artifact/tools.md)
- [Document Templates](artifact/templates.md)
- [Advanced PDF Operations](artifact/advanced.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with Python, HTML, CSS, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference-only guidance; the skill does not execute code, create files, make network requests, or access system files.]

## Skill Version(s):

1.0.1 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
