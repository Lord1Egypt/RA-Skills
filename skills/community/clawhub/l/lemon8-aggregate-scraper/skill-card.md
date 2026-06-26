## Description: <br>
Lemon8 内容数据查询助手，覆盖搜索、发现页、帖子详情、用户信息、评论、话题和热搜等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, brands, and cross-border commerce teams use this skill to search Lemon8 content, inspect posts and users, collect comments and topic information, and summarize lifestyle trends from MaxHub API results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Lemon8 searches, links, user IDs, post IDs, and related lookup parameters to MaxHub/aconfig.cn using a sensitive API key. <br>
Mitigation: Install only if this third-party API sharing is acceptable, configure the API key as a secret, and avoid entering data that should not be sent to MaxHub. <br>
Risk: Security evidence flags weak privacy scoping and fallback references to unrelated Douyin endpoints. <br>
Mitigation: Constrain use to documented /api/v1/lemon8/ endpoints and review or remove unrelated fallback behavior before normal approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/new-ironman/lemon8-aggregate-scraper) <br>
- [MaxHub API website](https://www.aconfig.cn) <br>
- [Post & User API](references/api-post-user.md) <br>
- [Search & Discover API](references/api-search-discover.md) <br>
- [Parameter Mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with tables, links, inline shell commands, and API result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English or Chinese output matched to the user; API key values should not be echoed.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
