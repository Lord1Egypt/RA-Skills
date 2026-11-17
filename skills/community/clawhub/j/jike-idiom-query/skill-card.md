## Description:

成语词典，支持搜索成语、查询成语详情、随机成语和成语接龙，并返回成语、拼音、解释、出处、例句、故事、用法、近义词和反义词。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese idiom questions, search idioms by keyword, retrieve idiom details, generate random idioms, and support idiom-chain interactions using Jike API data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The endpoint override can send the Jike API key to an arbitrary URL.

Mitigation: Leave JIKE_API_BASE_URL unset unless the destination is fully trusted, and rotate the key if it may have been sent to an untrusted endpoint.

Risk: The API key may be exposed through command-line history, process listings, or logs if passed directly as an argument.

Mitigation: Provide the key through JIKE_IDIOM_QUERY_KEY or JIKE_APPKEY rather than the --key argument.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-idiom-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Jike idiom query API endpoint](https://api.jikeapi.cn/v1/idiom/query)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text tables or JSON returned by a Python CLI command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Jike API key from JIKE_IDIOM_QUERY_KEY or JIKE_APPKEY; the API base URL defaults to api.jikeapi.cn unless overridden.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
