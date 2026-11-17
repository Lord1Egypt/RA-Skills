## Description:

Generates non-advisory Jukan-style investment analysis for stocks, industries, and markets using trend identification, bottleneck positioning, technical verification, and source rating.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kooui](https://clawhub.ai/user/kooui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to produce structured, bilingual investment-style research on equities, industries, and markets. The output is informational and is expected to include source-rating, uncertainty, and not-investment-advice disclaimers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an assistant to perform web searches for financial research and produce investment-style reports.

Mitigation: Use it only for non-advisory research workflows and require clear DYODD and not-investment-advice disclaimers in outputs.

Risk: Optional authenticated X.com scraping may involve reusable session cookies.

Mitigation: Avoid exporting or storing X.com cookies; if authentication is necessary, use a dedicated low-privilege account and secure temporary credential storage.

Risk: Optional Word report generation depends on an unpinned Python package.

Mitigation: Use a virtual environment and pin dependencies before enabling .docx report generation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kooui/skills/jukan-investment-strategy)
- [Jukan Five-Layer Analysis Framework](references/jukan_framework_universal.md)
- [Jukan05 Writing Style Examples](references/jukan_style_guide.md)
- [Jukan05 Knowledge Base Index](references/jukan_views/_index.md)
- [Jukan05 Sample Analysis Report](references/jukan05_full_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown/text analysis with an optional .docx report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include non-investment-advice and DYODD disclaimers.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
