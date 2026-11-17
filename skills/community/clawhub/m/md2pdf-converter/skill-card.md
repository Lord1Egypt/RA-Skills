## Description:

Converts Markdown documents to PDF using Pandoc, WeasyPrint, Chinese font fallbacks, and a local Twemoji cache for colorful emoji rendering after initial setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianxingleo](https://clawhub.ai/user/tianxingleo)

### License/Terms of Use:


## Use Case:

Developers and document authors use this skill to convert Markdown reports or documents into PDF files with CJK text support, page styling, code blocks, tables, and colorful emojis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-run setup downloads an unverified Twemoji archive from GitHub before extracting cached assets.

Mitigation: Review the download source before installation and prefer a release that verifies the archive checksum before extraction.

Risk: The conversion script invokes the emoji mapping helper through a developer-specific absolute path.

Mitigation: Use or request a version that resolves the bundled helper by relative path from the installed skill directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianxingleo/skills/md2pdf-converter)
- [Twemoji 14.0.0 archive](https://github.com/twitter/twemoji/archive/refs/tags/v14.0.0.tar.gz)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands; PDF files when the conversion script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [First run downloads and caches about 150 MB of Twemoji PNG assets; later conversions use the local cache.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
