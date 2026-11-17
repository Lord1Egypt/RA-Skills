## Description:

查询指定日期、月份或年份的节假日和调休安排，并返回假期名称、上班/放假状态和调休目标日期。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer holiday and calendar questions by querying Jike API for a day, month, or year.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Holiday/date query data and the Jike AppKey are sent to the API provider.

Mitigation: Use the skill only when that data sharing is acceptable, store the AppKey in environment variables, and treat logs or shell history containing the key as sensitive.

Risk: The API base URL can be changed through JIKE_API_BASE_URL.

Mitigation: Leave JIKE_API_BASE_URL unset or lock it to the intended HTTPS Jike API host before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-calendar-holiday-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Holiday day API endpoint](https://api.jikeapi.cn/v1/calendar/holiday/day)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [Plain text result or JSON response from a command-line query]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Jike AppKey configured through JIKE_CALENDAR_HOLIDAY_QUERY_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
