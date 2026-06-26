## Description: <br>
LinkedIn 职场数据查询助手，覆盖用户资料、公司信息、职位搜索、帖子、评论、广告等数据查询，并支持 V1/V2 API 路由。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, recruiting, strategy, and business-analysis users can query LinkedIn-derived company, profile, hiring, post, comment, and ad data through MaxHub APIs. The skill supports browse, analysis, comparison, and multi-endpoint reporting workflows for commercial intelligence and talent-market research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive MaxHub API credentials. <br>
Mitigation: Store MAXHUB_API_KEY as a secret, do not print or paste token values into responses, and install only when the MaxHub API provider is trusted. <br>
Risk: The skill can query LinkedIn-derived personal-profile and business data, which may support bulk profiling or unsolicited contact collection. <br>
Mitigation: Limit use to appropriate business-intelligence, recruiting, and analysis workflows, and avoid bulk profiling or unsolicited contact collection. <br>
Risk: The security summary flags unrelated fallback routes that users should review before enabling the skill. <br>
Mitigation: Review fallback and downgrade instructions before deployment and disable or constrain any non-LinkedIn behavior that is not needed for the intended use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/new-ironman/linkedin-aggregate-scraper) <br>
- [MaxHub API provider](https://www.aconfig.cn) <br>
- [Company Data API](references/api-company.md) <br>
- [User Data API](references/api-user.md) <br>
- [Search and Jobs API](references/api-search-jobs.md) <br>
- [Content and Ads API](references/api-content.md) <br>
- [Parameter Mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with tables, summaries, links, and inline curl command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include LinkedIn-derived profile, company, job, post, comment, ad, comparison, and analysis summaries; API access requires MAXHUB_API_KEY.] <br>

## Skill Version(s): <br>
3.6.1 (source: skill metadata and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
