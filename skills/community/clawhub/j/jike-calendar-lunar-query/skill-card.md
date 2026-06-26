## Description: <br>
Queries JikeAPI for Chinese lunar calendar and almanac details from a Gregorian date and optional time, including auspicious and inauspicious activities, zodiac, solar terms, festivals, and deity directions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer date-specific Chinese lunar calendar and old-almanac questions, such as whether a date is suitable for weddings, moving, or other activities. The skill formats a Gregorian date and optional time, calls the calendar API, and returns human-readable text or JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Date and time query values are sent to an external calendar API. <br>
Mitigation: Use the skill only when sharing those query values with the API provider is acceptable. <br>
Risk: The API key may appear in request URLs or logs. <br>
Mitigation: Set the key through a trusted environment and treat JIKE_CALENDAR_LUNAR_QUERY_KEY or JIKE_APPKEY as a secret. <br>
Risk: Overriding the API base URL can redirect requests and credentials to another endpoint. <br>
Mitigation: Avoid setting JIKE_API_BASE_URL unless the endpoint is controlled and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-calendar-lunar-query) <br>
- [JikeAPI homepage](https://www.jikeapi.cn/) <br>
- [JikeAPI lunar calendar detail endpoint](https://api.jikeapi.cn/v1/calendar/lunar/detail) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text or JSON from a Python CLI, with setup and invocation guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an API key in JIKE_CALENDAR_LUNAR_QUERY_KEY or JIKE_APPKEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
