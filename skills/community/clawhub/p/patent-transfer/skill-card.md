## Description:

智慧芽专利资产运营转化专家 — 基于输入的专利号，调用专利检索、语义检索、企业情报、新闻资讯 MCP，识别潜在转化企业并生成可直接推送的专利成果转化简报 HTML。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent operations, technology transfer, and business development teams use this skill to analyze patent packages, identify potential transferee companies, and generate a business-ready HTML transfer intelligence brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends patent numbers, company names, and industry context to configured external data providers.

Mitigation: Confirm the PatSnap/Zhihuiya MCP authorization scope and data-sharing acceptability before installation or use.

Risk: Generated patent-transfer reports may contain business-sensitive internal material.

Mitigation: Handle generated HTML briefs according to internal confidentiality and distribution controls.

Risk: Patent events, company intelligence, and news signals may be incorrect or stale when used for outreach decisions.

Mitigation: Verify cited patent events, news, and source links before contacting potential transferees.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/patent-transfer)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [HTML report with structured patent-package analysis, candidate company profiles, source-linked events, and action recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured PatSnap/Zhihuiya MCP services for real patent, company, and news retrieval; without those services it can only provide an analysis framework.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
