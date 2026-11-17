## Description:

查询指定日期的公历、农历、星座、生肖、黄历要点与节假日。当用户说：明天农历几号？今年春节是哪天？或类似万年历问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to answer Chinese calendar, lunar date, zodiac, almanac, and statutory holiday questions through JisuAPI calendar lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar queries and the configured API key are sent to JisuAPI.

Mitigation: Use a dedicated, low-privilege JISU_API_KEY and avoid sending sensitive free-form context.

Risk: Quota, billing, permission, or provider availability issues can cause lookup failures.

Mitigation: Monitor JisuAPI quota and handle API error responses before relying on answers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisu-calendar)
- [JisuAPI calendar documentation](https://www.jisuapi.com/api/calendar/)
- [JisuAPI website](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON from the calendar script, with Markdown guidance and shell commands in the skill instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; transmits calendar query parameters to JisuAPI.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
