## Description:

按年度汇总公司新授权专利及发明人，并依据公司制度或法定最低标准生成奖励参考清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

企业知识产权和人力资源团队可按授权公告年份统计新授权专利、核对每件专利的发明人，并按公司奖励制度或法定最低标准整理奖励参考清单。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API keys and cached data require security review; company names and search criteria are sent to PatentMax.

Mitigation: Use a limited service key supplied outside chat, review HTTPS destination and redirect restrictions and cache-path containment, and agree on query costs before searching. Keep internal reward policies local.

Risk: Generated award amounts may be inaccurate or inconsistent with current company policy or applicable requirements.

Mitigation: Have the responsible team verify the figures and governing reward standard before using the report for payments.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ip930/skills/inventor-reward-stats)
- [PatentMax API](https://api.ip930.com)

## Skill Output:

**Output Type(s):** [Files, Tables, Guidance]

**Output Format:** [UTF-8 CSV files with patent-level and inventor-level reward tables, plus a concise summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Award amounts are reference calculations; confirm company policy and applicable law before payment.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
