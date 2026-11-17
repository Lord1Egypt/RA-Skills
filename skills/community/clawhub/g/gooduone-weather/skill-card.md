## Description:

查询城市天气情况。使用场景：用户询问某个城市的天气、温度、或天气预报时。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gooduone](https://clawhub.ai/user/gooduone)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query current weather, temperature, or forecast information for a named city and return the result in Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather queries are sent to wttr.in, which can expose the requested city or location context to that service.

Mitigation: Use the skill only when sharing the queried city with wttr.in is acceptable.

Risk: Examples omit an explicit URL scheme, which can make transport behavior less clear to reviewers and users.

Mitigation: Prefer explicit https://wttr.in URLs when adapting or executing the examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gooduone/skills/gooduone-weather)
- [wttr.in weather service](https://wttr.in)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON, guidance]

**Output Format:** [Markdown with inline bash commands and optional plain text or JSON weather results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese-language weather output with lang=zh, concise one-line responses with format=3, and JSON output with format=j1.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
