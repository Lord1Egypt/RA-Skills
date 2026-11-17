## Description:

查十二星座列表与每日/周/月/年运势。当用户说：天蝎座今天运势？双子座本周财运？或类似星座运势问题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch the 12 star-sign list and retrieve daily, weekly, monthly, and yearly horoscope results from JisuAPI for conversational answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a JisuAPI AppKey and sends limited horoscope query data to JisuAPI.

Mitigation: Install only when outbound requests to JisuAPI are acceptable, keep the key in JISU_API_KEY, and avoid exposing it in prompts or logs.

Risk: Returned icon URLs may use plain HTTP.

Mitigation: Avoid auto-loading icon URLs unless the client proxies, upgrades, or filters them safely.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/jisu-astro)
- [JisuAPI Astro API Documentation](https://www.jisuapi.com/api/astro/)
- [JisuAPI Website](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON API results summarized as natural-language text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JISU_API_KEY and outbound requests to JisuAPI.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
