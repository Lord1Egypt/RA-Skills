## Description: <br>
皮皮虾数据查询助手，支持作品详情、用户数据、搜索、热搜、评论和话题查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content, operations, and research teams use this skill to query PiPiXia posts, users, comments, topics, search results, and trending data through the MaxHub API. It helps produce browsable results, comparisons, and data-driven summaries in Chinese or English. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a MaxHub API key and sends requests to aconfig.cn. <br>
Mitigation: Install only when the user trusts MaxHub/aconfig.cn with the API key, keep credentials out of responses, and review the skill before deployment. <br>
Risk: Security review notes metric-changing, generic short-link, and cross-platform fallback behavior that does not fit the claimed read-only scope. <br>
Mitigation: Avoid or remove documented view-count and arbitrary short-link behavior, narrow endpoints to PiPiXia, and make the read-only claim match the actual capabilities before relying on it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/new-ironman/pipixia-aggregate-scraper) <br>
- [MaxHub API Service](https://www.aconfig.cn) <br>
- [Post & User API](artifact/references/api-post-user.md) <br>
- [Search & Trending API](artifact/references/api-search-trending.md) <br>
- [Parameter Mappings](artifact/references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with tables, summaries, and inline curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and curl; output language follows the user's detected language.] <br>

## Skill Version(s): <br>
3.6.1 (source: evidence.release.version and SKILL.md metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
