## Description: <br>
Instagram 全场景数据查询助手，支持 V1/V2/V3 API 查询用户信息、帖子、Reels、Stories、评论、搜索、话题和地点数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, content creators, and social-media analysts use this skill to query Instagram profiles, posts, comments, hashtags, locations, and related engagement signals through MaxHub APIs for monitoring, influencer evaluation, and content research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive MaxHub API key and sends Instagram queries to a third-party service. <br>
Mitigation: Install only when that service is intended, store the API key in a secret or managed config store, and keep credential values out of prompts and outputs. <br>
Risk: Broad collection of personal, social-graph, or location data can create privacy and compliance obligations. <br>
Mitigation: Use the skill only with a legitimate basis, limit collection to the stated purpose, and avoid unnecessary bulk collection. <br>
Risk: The artifact includes non-Instagram fallback instructions that could cause confusing or unintended endpoint choices. <br>
Mitigation: Review fallback behavior before use and be explicit that intended requests are for Instagram data. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/new-ironman/instagram-aggregate-scraper) <br>
- [MaxHub API website](https://www.aconfig.cn) <br>
- [User Data API / 用户数据接口](references/api-user.md) <br>
- [Post Data API / 帖子数据接口](references/api-post.md) <br>
- [Search & Explore API / 搜索与发现接口](references/api-search.md) <br>
- [Parameter Mappings / 参数映射](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance, Analysis] <br>
**Output Format:** [Markdown responses with optional curl commands and tabular analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MAXHUB_API_KEY for authenticated read-only MaxHub API queries.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
