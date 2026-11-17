## Description:

十万个为什么。支持按问题关键词搜索，也支持随机返回问题和答案。适用场景：用户要求搜索、随机推荐或解释相关中文内容时使用。数据由即刻数据（jikeapi.cn）开放接口提供。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to search Chinese "Ten Whys" question-and-answer content by keyword or request a random question-and-answer pair from Jike API data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports an endpoint override that could send the Jike API key and user queries to an arbitrary host.

Mitigation: Use a dedicated limited-quota Jike API key, leave JIKE_API_BASE_URL unset unless the destination is fully trusted, and restrict outbound network access to the intended Jike API host.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-tenwhy-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Ten Whys query API endpoint](https://api.jikeapi.cn/v1/tenwhy/query)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text table output by default, with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JIKE_TENWHY_QUERY_KEY or JIKE_APPKEY credential; query mode accepts keyword, page, and page-size parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
