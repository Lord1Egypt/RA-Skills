## Description:

通过聚合数据（juhe.cn）API 查询中国各省市 92 号、95 号、98 号汽油和 0 号柴油的当日价格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query current mainland China oil prices by province or city for 92, 95, and 98 octane gasoline and 0 diesel. It can return nationwide results or filter by a city/province keyword, then present a table and JSON result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill sends the required Juhe API key over unencrypted HTTP.

Mitigation: Prefer an HTTPS-capable API endpoint or version before using a real key; avoid command-line key arguments, keep scripts/.env private, and rotate any key already used through the documented HTTP endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-oil-price)
- [Juhe oil price API documentation](https://www.juhe.cn/docs/api/id/540)
- [Juhe data platform](https://www.juhe.cn)
- [Juhe oil price API endpoint](http://apis.juhe.cn/gnyj/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell commands, tabular text output, and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JUHE_OIL_KEY credential; supports optional city/province filtering.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
