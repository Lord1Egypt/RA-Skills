## Description:

Litigation Risk Monitor helps agents monitor patent litigation risk for named assignees by combining litigated-patent discovery, INPADOC family expansion, case analysis, inventor trend review, and HTML/JSON/CSV report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent, legal-operations, and competitive-intelligence users provide one or more target assignees so an agent can gather litigation signals, expand patent families, analyze case and inventor trends, and produce a target-centered litigation risk report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target company names, patent terms, and watchlist-like inputs may be sent to external patent and search services.

Mitigation: Avoid confidential targets unless approved, and treat generated litigation reports as sensitive documents.

Risk: Generated HTML reports may contact third-party domains when opened.

Mitigation: Review reports before hosting or sharing, and prefer allowlisted URLs and integrity-pinned external assets for operational use.

Risk: Weak HTML-safety controls may allow unsafe or misleading content to appear in generated reports.

Mitigation: Escape untrusted text, review generated HTML, and scan outputs before deployment or distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/litigation-risk-monitor)
- [PatSnap Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, html, json, csv, guidance]

**Output Format:** [Single HTML report with embedded data and images, plus structured JSON and CSV attachments.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses target assignees with optional inventor lookback, family scope, and per-assignee patent limits; generated reports should be reviewed before sharing.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
