## Description:

Generates a self-contained HTML profile report that analyzes an inventor and organization using patent data, producing innovation capability ratings, patent metrics, risk sections, and representative patent tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External business users such as bank credit managers, HR teams, investors, and patent analysts use this skill to generate inventor-level innovation capability profile reports from patent data. The report is intended to support review workflows, not replace human validation of credit, hiring, or investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision-focused ratings may be inaccurate or misleading when used for lending, hiring, or investment decisions.

Mitigation: Verify generated ratings and recommendations against source patent data and applicable human review policies before relying on the report.

Risk: Sampling behavior can distort analytics when more than 100 patent records exist.

Mitigation: Require the full-pagination rule from SKILL.md and disregard latest-100 sampling guidance for analytics.

Risk: Generated HTML may include untrusted inventor, organization, or patent metadata.

Mitigation: Escape or sanitize all user-provided and patent metadata before opening, storing, or sharing generated HTML reports.

## Reference(s):

- [Data Collection Steps](references/data_collection_steps.md)
- [Key Data Summary Specification](references/key_data_summary_spec.md)
- [Report Design Specification](references/report_design_spec.md)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)
- [ClawHub Skill Release](https://clawhub.ai/yuanzhian-patsnap/skills/patent-inventor-profile-report)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Self-contained HTML report with inline CSS and JavaScript, plus Markdown guidance and report file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured Zhihuiya or PatSnap data access for live patent retrieval; generated decision-focused ratings should be checked against source data before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
