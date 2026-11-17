## Description:

按公历日期查询农历、宜忌、吉神凶煞等黄历信息，帮助代理回答搬家、领证、结婚等黄历择日问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up Chinese almanac details for a Gregorian date and summarize auspicious or inauspicious activities, lunar calendar information, zodiac, and related Huangli fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested dates and the API key are sent to JisuAPI.

Mitigation: Use a restricted JisuAPI key with low quota where possible, and avoid submitting sensitive context beyond the date required for lookup.

Risk: Huangli results may be mistaken for general scheduling, legal, medical, or other sensitive advice.

Mitigation: Frame outputs as almanac lookup results and avoid using the skill for sensitive advice unrelated to Huangli interpretation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/huangli)
- [JisuAPI Huangli API Documentation](https://www.jisuapi.com/api/huangli)
- [JisuAPI](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [JSON, Text guidance, Shell commands, Configuration]

**Output Format:** [JSON from the helper script, typically summarized by the agent as concise text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JISU_API_KEY environment variable; sends requested dates to JisuAPI.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
