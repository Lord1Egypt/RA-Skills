## Description:

输入阳历日期，查询道历日期、完整说明、道教节日、三会三元、八节、五腊、戊日等信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Agents serving users can use this skill to query Taoist calendar details for a Gregorian date through the Jike Data API. It is useful when a user asks for Taoist calendar dates, Taoist festivals, Sanhui/Sanyuan, Bajie, Wula, or Wu-day information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An undisclosed API endpoint override can redirect the user's AppKey to another server.

Mitigation: Do not set JIKE_API_BASE_URL unless the destination is intentionally controlled and trusted.

Risk: The AppKey can be exposed through command-line arguments or logs when passed with --key.

Mitigation: Prefer JIKE_CALENDAR_TAO_QUERY_KEY or JIKE_APPKEY environment variables for credential handling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jikeapi-cn/skills/jike-calendar-tao-query)
- [Jike Data Homepage](https://www.jikeapi.cn/)
- [Jike Data Tao Calendar API Endpoint](https://api.jikeapi.cn/v1/calendar/tao/detail)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Shell commands, Guidance]

**Output Format:** [Plain text or JSON returned from a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and an AppKey provided through JIKE_CALENDAR_TAO_QUERY_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
