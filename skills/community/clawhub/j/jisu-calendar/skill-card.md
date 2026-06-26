## Description: <br>
查询指定日期的公历、农历、星座、生肖、黄历要点与节假日。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer natural-language calendar questions by querying JisuAPI for Gregorian dates, lunar calendar fields, zodiac details, almanac notes, and holiday schedules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a JisuAPI key and sends calendar requests to an external provider. <br>
Mitigation: Use a dedicated JisuAPI key, monitor quota and provider policy, and avoid sending sensitive context when only a date is needed. <br>
Risk: Calendar and holiday answers depend on the external JisuAPI service response. <br>
Mitigation: Surface API errors clearly and verify high-impact date or holiday decisions against an authoritative source before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/jisu-calendar) <br>
- [JisuAPI website](https://www.jisuapi.com/) <br>
- [JisuAPI calendar documentation](https://www.jisuapi.com/api/calendar/) <br>
- [JisuAPI calendar query endpoint](https://api.jisuapi.com/calendar/query) <br>
- [JisuAPI holiday endpoint](https://api.jisuapi.com/calendar/holiday) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the JISU_API_KEY environment variable; API results are returned from JisuAPI without additional transformation. Security guidance recommends using a dedicated key, monitoring quota and provider policy, and avoiding sensitive context when only a date is needed.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
