## Description: <br>
按公历日期查询农历、宜忌、吉神凶煞等黄历信息。当用户说：明天宜不宜搬家？这周五适合领证吗？或类似黄历择日时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up Chinese almanac details for a Gregorian date, including lunar date, zodiac, auspicious and inauspicious activities, directional fortune data, and related Huangli fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each lookup sends the configured JisuAPI AppKey and requested date to JisuAPI, which may affect provider logs, quota, or billing. <br>
Mitigation: Use a JisuAPI key intended for this workflow, monitor provider usage, and avoid querying dates that reveal sensitive user intent when that matters. <br>
Risk: The skill depends on an external API and may fail when the key is missing, expired, unauthorized, rate-limited, or the provider service is unavailable. <br>
Mitigation: Check JISU_API_KEY configuration and handle API error codes or request failures before relying on the returned almanac result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/huangli) <br>
- [JisuAPI Huangli API documentation](https://www.jisuapi.com/api/huangli) <br>
- [JisuAPI website](https://www.jisuapi.com/) <br>
- [JisuAPI Huangli date endpoint](https://api.jisuapi.com/huangli/date) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API result interpreted as human-facing Markdown or text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the JISU_API_KEY environment variable; each query uses year, month, and day.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
