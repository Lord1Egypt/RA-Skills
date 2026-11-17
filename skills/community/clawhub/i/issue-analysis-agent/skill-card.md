## Description:

Issue Analysis Agent analyzes customer-service issue spreadsheets, generates weekly trend summaries and visual reports, and can upload the resulting report to a public COS URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidunderwood7970](https://clawhub.ai/user/davidunderwood7970)

### License/Terms of Use:

MIT-0

## Use Case:

Support, operations, and product teams use this skill to turn weekly customer-service Excel exports into issue metrics, unresolved-owner lists, trend summaries, alerts, and shareable reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled cloud credentials can allow unauthorized access or misuse if installed or run as-is.

Mitigation: Revoke and replace the COS credentials before use, load secrets from a managed secret store or environment variables, and keep credentials out of skill artifacts.

Risk: The workflow can publish customer, employee, or internal support reports to a public URL.

Mitigation: Disable public-read upload by default, require explicit approval for public sharing, and review or redact reports before upload.

Risk: Tests and validation paths can perform real network requests against COS.

Mitigation: Use synthetic local fixtures and mock or gate network upload during tests and pre-deployment checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidunderwood7970/skills/issue-analysis-agent)
- [Example week 12 report](https://claw-1301484442.cos.ap-shanghai.myqcloud.com/reports/issue_analysis/report_cn_latest.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON data files, Markdown summaries, HTML reports, public report URLs, and console text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform network upload and public-read publication when COS upload is enabled.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
