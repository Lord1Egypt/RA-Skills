## Description:

整合医药企业管线、专利、交易和战略竞争情报，帮助分析目标医药企业的研发管线、专利、交易、合作、组织和战略动向。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Business development, competitive intelligence, investment, and account-planning teams use this skill to research a named pharmaceutical or biotech company and generate an evidence-backed intelligence profile. It covers pipelines, clinical progress, patents, patent value, ADMET signals, competitors, financing, China market patent risk, and decision-oriented findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional PDF, PPT, or DOCX research documents may be read and incorporated into the generated report.

Mitigation: Upload only documents whose contents are intended to be used in the report, and avoid confidential materials unless that use is acceptable.

Risk: Clinical, patent, financing, and market intelligence can become stale or misleading if source validation is skipped.

Mitigation: Use current web, patent, paper, and PatSnap-style tool results, keep source tags on key facts, and review the data verification appendix before acting on the report.

Risk: ADMET and patent valuation sections depend on specialized PatSnap-style tools being available.

Mitigation: If those tools are unavailable, mark the affected section as skipped or incomplete and rerun after enabling the required tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/pharma-company-intelligence)
- [Publisher profile](https://clawhub.ai/user/yuanzhian-patsnap)

## Skill Output:

**Output Type(s):** [text, code, guidance, configuration]

**Output Format:** [Self-contained HTML report with source-tagged tables, structured prose, and inline CSS]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes an HTML report to @session/reports/<company_slug>_intelligence_report.html by default.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
