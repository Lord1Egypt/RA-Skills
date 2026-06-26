## Description: <br>
输入阳历日期，查询佛历日期、完整说明、佛教节日、斋日、星宿和吉凶等信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to answer Gregorian-date lookup requests with Buddhist calendar details from the Jike API, including Buddhist festivals, fasting days, constellations, zodiac, and auspiciousness fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries send the requested date and a Jike AppKey to jikeapi.cn. <br>
Mitigation: Install only when this third-party API exchange is acceptable, and scope the AppKey to this service where possible. <br>
Risk: The script allows JIKE_API_BASE_URL to redirect requests to an alternate endpoint. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless the alternate endpoint is intentionally trusted. <br>
Risk: The script can read a local .env file beside the script. <br>
Mitigation: Store only the required Jike AppKey in that file and avoid placing unrelated secrets in the script directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-calendar-foto-query) <br>
- [Publisher profile](https://clawhub.ai/user/jikeapi-cn) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Buddhist calendar detail API](https://api.jikeapi.cn/v1/calendar/foto/detail) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text summary or JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_CALENDAR_FOTO_QUERY_KEY or JIKE_APPKEY credential.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
