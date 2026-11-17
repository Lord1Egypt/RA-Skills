## Description:

知识产权成果统计工作流程助手。结合智慧芽MCP工具，引导科技管理部门从数据采集、核验、分类、评级到汇总上报的全流程操作，输出台账、质量分级简报与上报材料。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

科技管理部门负责人、知识产权专员和研发管理人员 use this skill to run patent portfolio statistics workflows: collect and verify patent records, classify assets, apply S/A/B/C quality ratings, summarize annual or quarterly metrics, and prepare reporting or archive materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may process patent lists, project data, competitor names, and external reporting materials that can be business-sensitive.

Mitigation: Review and redact sensitive content before sharing generated reports or filing external materials.

Risk: Live patent retrieval depends on an authorized PatSnap/Zhihuiya MCP integration.

Mitigation: Install only when that integration is intended, confirm account authorization, and treat results as unavailable until the MCP tools are configured.

Risk: Patent status, citation, family, and quality-rating outputs can affect operational or reporting decisions.

Mitigation: Verify source attribution and reconcile database results against internal ledgers before updating official records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/ip-stat-workflow)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown tables, structured text, summaries, checklists, and reporting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured PatSnap/Zhihuiya MCP access for live patent retrieval; without it, outputs are limited to workflow guidance and analysis structure.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
