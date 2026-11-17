## Description:

皮皮虾（Pipixia）内容数据查询 skill，通过 MaxHub API 查询作品详情、统计、评论、首页流、搜索、热搜、话题和用户相关内容。适合内容研究、互动分析、热点追踪和素材筛选。所有请求发送到 https://www.aconfig.cn。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

面向内容创作者、运营人员和研究者，用于查询皮皮虾内容及互动数据，辅助选题、热点追踪和内容分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports undeclared local compliance records, update guidance, and an unpinned installer; reference resolution was partial, so the evidence is incomplete.

Mitigation: Before installation, review the compliance-state and audit-log writes, and verify the installer and update source and version. Treat the scan verdict as a review flag, not a finding of malicious intent.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-pipixia)
- [ClawHub release](https://clawhub.ai/xiewxx/skills/maxhub-pipixia-pro)
- [SkillHub listing](https://skillhub.cn/skills/pipixia-pro)
- [MaxHub API service](https://www.aconfig.cn)
- [Pipixia Open Platform](https://open.pipixia.com)
- [Endpoint whitelist](references/endpoints_whitelist.yaml)
- [Parameter mappings](references/param-mappings.md)
- [Query recipes index](references/recipes/_index.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON, Text, Markdown]

**Output Format:** [Natural-language summaries of MaxHub API responses, with structured JSON data when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAXHUB_API_KEY; requests are sent to https://www.aconfig.cn. Keep API keys and other credentials out of outputs.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
