## Description:

LinkedIn 职场数据查询助手，覆盖用户资料、公司信息、职位搜索、帖子、评论和广告查询，并支持 V1/V2 API。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, recruiting, HR, and strategy teams use this skill to gather LinkedIn business intelligence about people, companies, jobs, posts, comments, and ads through MaxHub APIs. It supports browse, analysis, and comparison workflows for company research, talent market analysis, and competitor monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic fallback instructions include unrelated Douyin endpoint paths that could send authenticated requests outside the expected LinkedIn scope.

Mitigation: Constrain requests to documented /api/v1/linkedin/ paths and audit or disable non-LinkedIn fallback mappings before deployment.

Risk: The skill requires a MaxHub API key and sends LinkedIn search or profile queries to www.aconfig.cn.

Mitigation: Use a dedicated API key, avoid submitting unnecessary sensitive data, and review third-party service terms before use.

Risk: Returned third-party data may be incomplete, restricted, stale, or inaccurate.

Mitigation: Treat results as reference data and verify important business, recruiting, or compliance decisions against authoritative sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/new-ironman/skills/linkedin-aggregate-scraper)
- [Publisher Profile](https://clawhub.ai/user/new-ironman)
- [MaxHub API Website](https://www.aconfig.cn)
- [User Data API](references/api-user.md)
- [Company Data API](references/api-company.md)
- [Search & Jobs API](references/api-search-jobs.md)
- [Content & Ads API](references/api-content.md)
- [Parameter Mappings](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, tables, and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese responses; API key values are not included in output.]

## Skill Version(s):

3.6.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
