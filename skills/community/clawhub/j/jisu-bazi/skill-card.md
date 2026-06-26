## Description: <br>
按出生时间与城市排八字，返回四柱、纳音、大运流年等。当用户说：1990 年 6 月生于北京八字排盘、看看大运流年，或类似八字排盘时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to produce Bazi chart data from a birth date, time, city, sex, and calendar options. It supports conversational summaries of four pillars, Na Yin, Da Yun, Liu Nian, and related chart fields for entertainment and learning reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birth-chart inputs and the configured API key are sent to JisuAPI. <br>
Mitigation: Use the skill only when sharing those details with JisuAPI is acceptable, prefer a nickname or blank display name when possible, and use a dedicated or easily rotated API key. <br>
Risk: Bazi chart interpretations may be mistaken for decision-making advice. <br>
Mitigation: Present outputs as entertainment and learning reference, not as a basis for financial, medical, legal, employment, or relationship decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jisuapi/jisu-bazi) <br>
- [JisuAPI Bazi API Documentation](https://www.jisuapi.com/api/bazi/) <br>
- [JisuAPI Homepage](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance, Shell commands, Configuration] <br>
**Output Format:** [JSON result data with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, and JISU_API_KEY; sends entered birth-chart details to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
