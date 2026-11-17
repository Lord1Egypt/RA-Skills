## Description:

读取 Amazon 已采集评论的关键词、星级与趋势统计，提炼买家常用词、痛点词、场景词和文案测试线索。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and market analysts use the skill to review collected customer comments for recurring buyer language, pain points, and use cases, then develop copy testing ideas grounded in the returned statistics.

### Deployment Geography for Use:

Amazon marketplaces in the United States, United Kingdom, Germany, Japan, Canada, France, Spain, and Italy

## Known Risks and Mitigations:

Risk: ARI receives the selected product identifiers, and authorization stores an API key locally.

Mitigation: Authorize only an ARI account you intend to use, keep the local key file private, and revoke the key when it is no longer needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/funewa/skills/keyword-radar)
- [ARI service](https://ari.funewa.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON statistics with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scoped by ASIN, marketplace, and time window; report sample limits. Keyword frequency is not search volume, CPC, rank, or conversion rate.]

## Skill Version(s):

1.5.3 (source: SKILL.md frontmatter; server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
