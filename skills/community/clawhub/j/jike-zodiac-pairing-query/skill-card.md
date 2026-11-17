## Description:

输入男生星座和女生星座，查询星座配对指数、比例、同情指数、天长地久指数、结果评述和恋爱建议，数据由即刻数据（jikeapi.cn）开放接口提供。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer zodiac compatibility questions by calling the Jike Data zodiac pairing API with boy_zodiac and girl_zodiac inputs. The skill returns Chinese text by default and can return structured JSON when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Zodiac query inputs and the Jike AppKey are sent to Jike API.

Mitigation: Install only when that data sharing is acceptable, and use a scoped or low-risk AppKey.

Risk: The skill allows JIKE_API_BASE_URL to override the default API host.

Mitigation: Avoid setting JIKE_API_BASE_URL unless the endpoint is trusted.

Risk: The AppKey is sent as a URL query parameter.

Mitigation: Do not log full request URLs and rotate the AppKey if it may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-zodiac-pairing-query)
- [Jike Data homepage](https://www.jikeapi.cn/)
- [Jike zodiac pairing API endpoint](https://api.jikeapi.cn/v1/zodiac_pairing)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Chinese plain text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JIKE_ZODIAC_PAIRING_QUERY_KEY or JIKE_APPKEY AppKey.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
