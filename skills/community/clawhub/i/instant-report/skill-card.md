## Description:

Generates structured industry, market, competitor, and company research reports from user requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianghaist](https://clawhub.ai/user/jianghaist)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to request structured company, industry, market, or competitive research reports. It is suited for report drafting workflows that need cited sources, fact-checking, Markdown working output, and final document deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad or English report requests may trigger the full multi-stage report process and may still produce Chinese output.

Mitigation: Set explicit scope, language, length, and deliverable expectations before invoking the skill.

Risk: Generated research reports can include stale, weakly sourced, or inconsistent market data if source quality is not checked.

Mitigation: Review source URLs, data cutoff dates, independent-source checks, and the fact-check findings before using the report for business decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jianghaist/skills/instant-report)
- [Skill Definition](artifact/SKILL.md)
- [Data Sources Reference](artifact/references/data_sources.md)
- [Report Structure Reference](artifact/references/report_structure.md)
- [Quality Checklist](artifact/references/quality_checklist.md)
- [Report Style Guide](artifact/references/style_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown reports with source lists and Mermaid chart blocks, plus DOCX and PDF deliverables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a fact-check report and corrected report text when issues are found.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
