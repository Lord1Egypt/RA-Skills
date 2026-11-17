## Description:

核查单个已授权公网 IPv4/IPv6 的归属、路由、信誉与代理/欺诈风控信号，默认本地处理，外部查询需明确确认。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianfuli](https://clawhub.ai/user/jianfuli)

### License/Terms of Use:

MIT

## Use Case:

Developers, security operators, and authorized business operators use this skill to review one owned, public, or explicitly authorized public IP address for registry, routing, geolocation, network-type, and reputation signals. The output supports human review for infrastructure checks, abnormal-request triage, provider delivery acceptance testing, and public-information verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External lookups can transmit the target IP address to provider domains and may involve cross-border transfer.

Mitigation: Use local-only mode by default; enable external lookups only after confirming the target IP, provider domains, sent fields, authorization, and data-handling requirements.

Risk: Generated reports can contain the complete IP address, geographic region, organization or ISP, route or allocation prefixes, and network-risk labels.

Mitigation: Store reports in a private directory with restrictive permissions, keep them out of public logs or issue trackers, and delete them under the operator's retention schedule.

Risk: IP reputation evidence can be incomplete, conflicting, or unsuitable for automatic decisions.

Mitigation: Use the report only as an aid for authorized human review, not as a legal conclusion, identity lookup, or automatic allow/deny decision.

## Reference(s):

- [README](README.md)
- [Provider Reference](references/providers.md)
- [Fusion Methodology](references/methodology.md)
- [Public-Page Evidence](references/public-pages.md)
- [HTML Report Design](references/report-design.md)
- [FAQ and Troubleshooting](references/faq.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Concise text summary plus optional local JSON, Markdown, or offline HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts exactly one public IPv4 or IPv6 address; default local-only mode makes no external requests.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
