## Description:

根据身份证号解析地区、出生日期、性别与校验位；可按城市查前六位规则。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese ID-card attribution questions, validate checksum status, derive birth date and sex fields, or look up the first six ID-card digits for a city.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ID-card queries may disclose sensitive national ID data to JisuAPI.

Mitigation: Avoid submitting full national ID numbers when a six-digit region code is enough, and obtain user consent before sending sensitive identifiers to the provider.

Risk: The JISU_API_KEY is sent in URL parameters and may appear in provider, proxy, or network logs.

Mitigation: Treat JISU_API_KEY as a secret, scope and rotate it regularly, and avoid running the skill through logging proxies that retain query strings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/idcard)
- [JisuAPI homepage](https://www.jisuapi.com/)
- [JisuAPI ID-card API documentation](https://www.jisuapi.com/api/idcard/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON responses summarized as agent-facing text or Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; calls JisuAPI endpoints for ID-card and city-code lookup.]

## Skill Version(s):

1.0.3 (source: server evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
