## Description:

国内猪肉价格实时查询。按省份查询白条肉、精瘦肉、土杂猪、外三元、内三元价格，也支持不传省份返回全部地区价格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query current pork prices by Chinese province or nationwide and return tabular or JSON results for carcass pork, lean pork, native pigs, and hybrid pigs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An undocumented API endpoint override can redirect the configured AppKey to another host.

Mitigation: Install only after review in environments where untrusted users, wrappers, or deployment settings can influence environment variables; use a narrowly scoped Jike AppKey and prefer a version that pins outbound requests to the documented Jike API host.

Risk: The required AppKey may be exposed if stored in shared files or broad environment scopes.

Mitigation: Avoid storing the AppKey in shared files and provide it through a narrowly scoped environment variable for the agent process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-pork-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Jike pork query API endpoint](https://api.jikeapi.cn/v1/pork/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal table or JSON, typically summarized in Markdown by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Jike AppKey provided through JIKE_PORK_QUERY_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
