## Description:

汉语词语查询，支持搜索词语、词语详情、随机词语、近义词查询和反义词查询，返回词语、拼音、解释、出处、例句、故事、用法、近义词和反义词。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent look up Chinese words, definitions, pinyin, citations, usage examples, synonyms, antonyms, and random word results through Jike API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an endpoint override that can send the AppKey and user queries to a non-Jike server if the environment is altered.

Mitigation: Use a dedicated low-privilege Jike AppKey, avoid passing the key on the command line, do not set JIKE_API_BASE_URL unless the endpoint is trusted, and limit outbound access to the official Jike API host where possible.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jikeapi-cn/skills/jike-word-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Jike word query API endpoint](https://api.jikeapi.cn/v1/word/query)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Plain text tables or JSON from a Python CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Jike AppKey supplied through JIKE_WORD_QUERY_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
