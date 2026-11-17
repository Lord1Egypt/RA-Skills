## Description:

输入星座名称后，查询星座特征、守护宫、阴阳性、守护星、幸运色、幸运数字、日期区间和男女特点，并返回中文文本或 JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent workflows use this skill to look up Chinese-language zodiac sign profile information from the Jike API when answering traditional culture, lifestyle, or compatibility questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API host can be overridden, which could send the user's Jike API key to a different server.

Mitigation: Review the skill before installing, avoid setting JIKE_API_BASE_URL, and prefer a version that pins or validates the API host.

Risk: The AppKey is sent as a URL query parameter.

Mitigation: Use only a Jike API key appropriate for this integration and prefer a version that avoids placing the AppKey in the URL query string.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-zodiac-sign-query)
- [Publisher profile](https://clawhub.ai/user/jikeapi-cn)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Jike zodiac API endpoint](https://api.jikeapi.cn/v1/zodiac_sign)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese plain text by default, or JSON when invoked with --json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Jike API key through JIKE_ZODIAC_SIGN_QUERY_KEY, JIKE_APPKEY, or the --key argument.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
