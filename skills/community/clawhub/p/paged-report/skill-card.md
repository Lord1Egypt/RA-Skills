## Description:

Generate client-facing HTML reports with A4-oriented print styles and optional browser-based PDF previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mfang0126](https://clawhub.ai/user/mfang0126)

### License/Terms of Use:

MIT

## Use Case:

Developers and client-facing teams use this skill to assemble structured proposals, progress reports, confirmations, audits, and handoff reports as printable HTML, then preview and verify an optional PDF before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client-facing reports may contain incorrect or sensitive content.

Mitigation: Review facts before sharing; exclude secrets and unreviewed customer information.

Risk: Browser preview uses a local WebBridge daemon and a temporary localhost server.

Mitigation: Use WebBridge only in a trusted local browser context and stop the temporary server after previewing.

Risk: HTML authoring boundaries may not match physical A4 pages in a PDF.

Mitigation: Inspect the rendered PDF for pagination, overflow, and footer placement before delivery.

## Reference(s):

- [Paged Report on ClawHub](https://clawhub.ai/mfang0126/skills/paged-report)
- [Report input schema](schemas/report.schema.json)

## Skill Output:

**Output Type(s):** [HTML files, PDF files, Report-generation guidance]

**Output Format:** [Self-contained HTML; optional A4 PDF preview]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Print layout and physical page count require verification in the target browser.]

## Skill Version(s):

1.2.1 (source: release metadata, frontmatter, pyproject.toml, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
