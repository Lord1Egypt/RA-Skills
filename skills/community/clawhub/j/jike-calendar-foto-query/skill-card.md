## Description:

输入阳历日期，查询佛历日期、完整说明、佛教节日、斋日、星宿和吉凶等信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and AI clients use this skill to look up Buddhist calendar details for a supplied Gregorian date, including Buddhist date text, festivals, fasting days, lunar mansion information, and auspiciousness notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send the configured API key to a request destination selected through JIKE_API_BASE_URL.

Mitigation: Run it only in an environment where JIKE_API_BASE_URL is unset or pinned to the trusted Jike API host.

Risk: The API key is included in the request URL query string.

Mitigation: Use a Jike API key scoped for this integration and avoid passing keys on the command line or through logged shell history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-calendar-foto-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Jike Buddhist calendar API endpoint](https://api.jikeapi.cn/v1/calendar/foto/detail)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON returned from a Python command-line helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Jike API key in JIKE_CALENDAR_FOTO_QUERY_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
