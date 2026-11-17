## Description:

Helps investors, advisors, analysts, and family-office operators review portfolio allocation, concentration risk, fees, rebalancing needs, and investment policy notes from brokerage exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External users, including individual investors, financial advisors, analysts, and family-office operators, use this skill to turn portfolio CSV exports or brokerage statements into practical allocation reviews, risk checklists, rebalancing notes, and plain-language investment policy support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit triggering may apply the workflow to general finance or operations phrasing.

Mitigation: Invoke it intentionally for portfolio-review tasks and check that the requested output is about allocation, risk, fees, rebalancing, or investment policy notes.

Risk: Brokerage exports and statements may contain sensitive personal, account, and holdings data.

Mitigation: Share only the fields needed for the review, redact account identifiers, and avoid uploading more brokerage data than necessary.

Risk: Portfolio analysis can be mistaken for personalized investment advice.

Mitigation: Treat outputs as decision support and verify recommendations with qualified financial judgment before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/portfolio-risk-allocation-reviewer)
- [Requirement Plan](references/requirement-plan.md)
- [Skill README](README.md)
- [FINC3017 Investment Management Analysis](https://segmentfault.com/a/1190000044097020)
- [MIE 1622H Risk-Based and Robust](https://segmentfault.com/a/1190000046223610)
- [Portfolio Recipe Export](https://wenku.csdn.net/doc/6jsund1a3y?ops_request_misc=elastic_search_misc&request_id=11d14a5b97df48ceb622c2f05fdca564&biz_id=&utm_medium=distribute.pc_search_result.none-task-c_download-2~all~ElasticSearch~search_v2-1-6jsund1a3y-null-null.142^v102^control&utm_term=portfolio%20allocation%20risk%20review%20rebalancing%20brokerage%20export)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown responses with optional checklists, templates, lightweight analysis, or local scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, and follow-up risks for portfolio review workflows.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
