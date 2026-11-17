## Description:

Operate API2PDF through an OOMOL-connected account to convert Markdown into PDFs and retrieve the generated PDF URL and conversion metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to convert Markdown documents into PDFs through their connected API2PDF account and retrieve the resulting file URL and conversion details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes downloaded CLI installer code and can synchronize skills; the installer contents are unverified.

Mitigation: Review and approve CLI installation and skill synchronization separately. Submit only documents intended for OOMOL and API2PDF to process, and confirm any conversion charges.

## Reference(s):

- [API2PDF API documentation](https://v2.api2pdf.com/explore.html)
- [API2PDF homepage](https://www.api2pdf.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [PDF files, JSON, Text]

**Output Format:** [PDF document and JSON response containing the generated URL and conversion metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts Markdown as input; the PDF is returned by URL.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
