## Description: <br>
支持查询某天是否放假或调休、某月假期、某年假期，返回假期名称、是否上班和调休目标日期。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to answer Chinese holiday and adjusted-workday questions for a specific day, month, or year using Jike API holiday data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JIKE_API_BASE_URL override can route requests and the Jike AppKey to a non-default endpoint. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless the endpoint is intentionally trusted, and use a low-scope Jike API key. <br>
Risk: Full request URLs include the AppKey as a query parameter. <br>
Mitigation: Avoid copying, logging, or sharing full request URLs and command output that may expose credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-calendar-holiday-query) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Jike calendar holiday API endpoint](https://api.jikeapi.cn/v1/calendar/holiday/day) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text tables or JSON from command-line API lookups] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a Jike API key in JIKE_CALENDAR_HOLIDAY_QUERY_KEY or JIKE_APPKEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
