## Description:

Screens high-value patent packages from PatSnap/Zhihuiya patent queries and generates a required HTML report with an optional Word report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent analysts use this skill to run a PatSnap/Zhihuiya search query, score returned patents with weighted high-value indicators, and produce an auditable screening package. It is intended for report generation, not legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent queries, identifiers, and report data are sent to Zhihuiya/PatSnap and stored in local trace/report files.

Mitigation: Use the skill only with data approved for PatSnap/Zhihuiya processing, run it in a dedicated folder, and protect generated JSON, spreadsheet, HTML, and DOCX files.

Risk: The optional Word report can fetch image URLs for abstract drawings.

Mitigation: Prefer the HTML report or run the Word step with image downloads disabled unless image hosts and size limits have been reviewed.

Risk: The skill relies on external Python dependencies and live API calls.

Mitigation: Pin dependencies in the execution environment and review API failures or unavailable fields in the trace output before relying on the report.

## Reference(s):

- [High-Value Patent Screening Standard](references/screening-standard.md)
- [ClawHub release page](https://clawhub.ai/yuanzhian-patsnap/skills/high-value-patent-package)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [HTML report, trace JSON or spreadsheet, and optional DOCX report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PatSnap/Zhihuiya API results; missing data is marked as unavailable and preserved in the trace output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
