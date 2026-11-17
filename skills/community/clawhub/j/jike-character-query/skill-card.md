## Description:

新华字典。支持拼音列表、部首列表、按拼音查汉字、按部首查汉字、汉字详情查询，返回汉字、拼音、部首、笔画、结构、繁体、异体字、同义词、反义词和形近字。适用场景：用户说“查一下好字怎么读”“口部有哪些汉字”“yī 这个拼音有哪些字”等。数据由即刻数据（jikeapi.cn）开放接口提供。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Xinhua-style Chinese dictionary data through Jike API, including pinyin lists, radical lists, character lookup by pinyin or radical, and single-character details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A manipulated JIKE_API_BASE_URL can redirect requests, including the Jike AppKey and query terms, to another host.

Mitigation: Run the skill only in trusted launch environments, keep the AppKey secret, and ensure JIKE_API_BASE_URL is not inherited from untrusted users or unsafe runtime contexts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jikeapi-cn/skills/jike-character-query)
- [Jike API Homepage](https://www.jikeapi.cn/)
- [Jike Character Detail API Endpoint](https://api.jikeapi.cn/v1/character/chinese/detail)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text summaries or pretty-printed JSON from a Python CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Jike AppKey through JIKE_CHARACTER_QUERY_KEY or JIKE_APPKEY; text output can be limited with --limit.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
