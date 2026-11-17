## Description:

比较技术领域不同 IPC 小组在两个时期的专利申请量，识别增长较快的新兴方向，并汇总代表专利与主要申请人。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

研发人员、企业分析师和投资决策者可用它比较专利申请趋势，筛选快速增长的技术细分方向，并查看代表专利和主要申请人。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API key handling and redirected requests need review.

Mitigation: Before supplying a paid key, require HTTPS-only requests, review safe redirect handling, store credentials in an owner-only file, and do not paste keys into chat.

Risk: Queries are sent to PatentMax and may incur fees.

Mitigation: Avoid including confidential invention details in queries and review the disclosed fees before running paid searches or statistics.

## Reference(s):

- [Patent Hotspots skill release](https://clawhub.ai/ip930/skills/patent-hotspots)
- [Publisher profile](https://clawhub.ai/user/ip930)
- [PatentMax service](https://ip930.com)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [Search workflow](references/search-workflow.md)
- [API reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [Files, Analysis, Guidance]

**Output Format:** [UTF-8 CSV (Excel-compatible)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes growth rates, representative patents, and leading applicants by IPC subgroup.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
