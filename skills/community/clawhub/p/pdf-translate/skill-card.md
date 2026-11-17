## Description:

Translates PDF documents to Chinese with professional typography by extracting text, translating section by section into structured Markdown, and generating PDF output with full CJK support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrislee121](https://clawhub.ai/user/chrislee121)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to translate English PDF documents into Chinese while preserving headings, tables, lists, code blocks, and other structure. It produces editable Markdown and a polished PDF when the required local dependencies are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering untrusted Markdown to PDF can unexpectedly load external or local resources.

Mitigation: Render only trusted Markdown, or run PDF generation with network and local-file access sandboxed or disabled.

Risk: A bundled legacy helper writes to a hardcoded personal output path.

Mitigation: Use the recommended md2pdf.py workflow, or change the legacy helper output path before running it.

Risk: The workflow processes local document contents and is designed for Chinese translation.

Mitigation: Use it only with documents suitable for local processing and confirm Chinese is the intended target language before translation.

## Reference(s):

- [Translation Standards](references/translation-standards.md)
- [Font Configuration](references/font-configuration.md)
- [Troubleshooting](references/troubleshooting.md)
- [Complete Example](references/complete-example.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; translated Markdown and PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese Markdown plus PDF output; PDF generation depends on local Python and system font/rendering dependencies.]

## Skill Version(s):

4.0.0 (source: evidence release metadata and CHANGELOG, released 2026-02-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
