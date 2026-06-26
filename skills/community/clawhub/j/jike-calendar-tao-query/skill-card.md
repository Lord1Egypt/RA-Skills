## Description: <br>
输入阳历日期，查询道历日期、完整说明、道教节日、三会三元、八节、五腊、戊日等信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to convert a Gregorian date into Taoist calendar details from the Jike API. It is intended for Taoist calendar/date lookup workflows that need a concise text answer or raw JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an API key in URL-based network calls, which can expose credentials through logs or shared request URLs. <br>
Mitigation: Use a low-scope Jike AppKey, avoid logging or sharing full request URLs, and keep credentials in the documented environment variables. <br>
Risk: The skill has broad wording that could trigger it for unrelated requests. <br>
Mitigation: Use it only for Taoist calendar/date lookups and confirm the user supplied a Gregorian date before execution. <br>
Risk: The API base URL can be overridden through JIKE_API_BASE_URL. <br>
Mitigation: Set JIKE_API_BASE_URL only when it points to a trusted HTTPS Jike endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-calendar-tao-query) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Taoist calendar detail API endpoint](https://api.jikeapi.cn/v1/calendar/tao/detail) <br>
- [Publisher profile](https://clawhub.ai/user/jikeapi-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON, typically returned with concise Markdown guidance and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, a Jike AppKey, and a Gregorian date in YYYY-MM-DD format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
