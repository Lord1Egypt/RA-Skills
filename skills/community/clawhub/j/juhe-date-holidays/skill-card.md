## Description: <br>
This skill helps agents query Juhe Data for date-specific holiday status, adjusted workdays, weekday, lunar calendar, and almanac details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to answer whether a requested date is a holiday or adjusted workday and to return related lunar-calendar and almanac information from Juhe Data. <br>

### Deployment Geography for Use: <br>
Global, with content focused on China holiday and lunar-calendar data. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a required Juhe API key in ways that could expose it, including command-line key passing and a local scripts/.env file. <br>
Mitigation: Prefer a protected JUHE_DATE_HOLIDAY_KEY environment variable, avoid command-line key passing, and do not commit scripts/.env. <br>
Risk: The artifact uses Juhe's HTTP calendar endpoint for API calls. <br>
Mitigation: Check whether Juhe supports an HTTPS version of the endpoint before using the included script in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-date-holidays) <br>
- [Juhe holiday API documentation](https://www.juhe.cn/docs/api/id/606) <br>
- [Juhe Data](https://www.juhe.cn) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/juhemcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance, shell commands, formatted text, and JSON API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a Juhe API key supplied through JUHE_DATE_HOLIDAY_KEY, scripts/.env, or the --key command-line option.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
