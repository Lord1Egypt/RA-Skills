## Description:

输入阳历日期和时间，查询农历日期、黄历宜忌、黄黑道、吉神凶煞、生肖、星座、节气、喜神福神财神方位等信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and AI agents use this skill to look up Chinese lunar calendar and almanac details for a specified Gregorian date and optional time. It supports questions about lunar dates, auspicious and inauspicious activities, zodiac details, solar terms, festivals, and deity directions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JikeAPI AppKey and requested date or time are sent to a third-party service.

Mitigation: Use a low-privilege AppKey and avoid sending sensitive or unnecessary query context.

Risk: Supplying the AppKey with --key may expose it through shell history or process listings.

Mitigation: Prefer environment variables such as JIKE_CALENDAR_LUNAR_QUERY_KEY or JIKE_APPKEY for credential configuration.

Risk: Changing JIKE_API_BASE_URL can redirect requests, including the AppKey, to another endpoint.

Mitigation: Leave JIKE_API_BASE_URL unset unless the endpoint is fully trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-calendar-lunar-query)
- [JikeAPI homepage](https://www.jikeapi.cn/)
- [JikeAPI lunar calendar detail endpoint](https://api.jikeapi.cn/v1/calendar/lunar/detail)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON returned from a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JikeAPI AppKey supplied through JIKE_CALENDAR_LUNAR_QUERY_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
