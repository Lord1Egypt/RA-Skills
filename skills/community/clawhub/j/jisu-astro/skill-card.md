## Description: <br>
Looks up the 12 zodiac signs and retrieves daily, weekly, monthly, and yearly horoscope data through JisuAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to answer user questions about zodiac sign ranges and horoscope forecasts for today, tomorrow, this week, this month, or this year. It is intended for users who ask horoscope questions such as daily fortune, love, career, money, or health outlooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a JisuAPI AppKey and sends horoscope lookup parameters such as zodiac sign ID and query date to JisuAPI. <br>
Mitigation: Use the skill only where JisuAPI calls are acceptable, keep JISU_API_KEY out of logs and shared outputs, and rotate the key if it is exposed. <br>
Risk: Users may provide full birthdays or extra personal details when asking horoscope questions. <br>
Mitigation: Send only the zodiac sign ID and query date needed for the lookup, and avoid collecting or forwarding unnecessary personal details. <br>


## Reference(s): <br>
- [JisuAPI homepage](https://www.jisuapi.com/) <br>
- [JisuAPI astrology API documentation](https://www.jisuapi.com/api/astro/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses from the astrology API, with agent-authored natural-language summaries when used in conversation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends zodiac sign ID and optional query date to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
