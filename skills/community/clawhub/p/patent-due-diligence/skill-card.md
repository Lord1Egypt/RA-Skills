## Description:

核查目标公司的专利数量、权属转让、质押与许可，并整理尽调清单和风险摘要。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

投资、并购及合作前，尽调人员可用它核查企业专利组合、权属流转及相关法律事件，并整理清单和风险摘要。它仅覆盖专利数据核查，不替代正式法律尽调。

### Deployment Geography for Use:

中国、美国、欧洲、日本、韩国及 WIPO（按技能文档所列数据覆盖范围）

## Known Risks and Mitigations:

Risk: API-key handling and cache boundaries warrant review.

Mitigation: Prefer a corrected version; if evaluating this release, use an isolated environment and private cache directory, restrict the API key to limited credit, and do not paste production credentials into chat.

Risk: Retrying timed-out patent requests may create unexpected charges.

Mitigation: Check account charges before retrying, and provide only authorized query information.

## Reference(s):

- [PatentMax API reference](references/api-reference.md)
- [Patent search workflow](references/search-workflow.md)
- [Search query construction](references/query-construction.md)
- [PatentMax API and console](https://api.ip930.com)

## Skill Output:

**Output Type(s):** [Analysis, CSV, Text]

**Output Format:** [Chinese-language risk summary and UTF-8 CSV patent due diligence checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Patent database findings only; records may lag the official register and do not constitute legal advice, patent valuation, or infringement analysis.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
