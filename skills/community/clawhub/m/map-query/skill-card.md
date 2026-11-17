## Description:

Query nearby restaurants, shops, promotions, and points of interest by address using AMap, Baidu Maps, or Tencent Maps with geocoding and filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uynewnas](https://clawhub.ai/user/uynewnas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill through an agent to geocode addresses and find nearby food, promotions, shops, and other points of interest through configured map provider API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured map API keys may be exposed through output, chats, or logs.

Mitigation: Use restricted, low-quota API keys, avoid pasting or printing key values, and rotate any key that may already have been exposed.

Risk: Addresses and coordinates are sent to AMap, Baidu Maps, or Tencent Maps.

Mitigation: Inform users before sending location-bearing requests and avoid querying sensitive personal locations unless the user intends that disclosure.

Risk: The scripts may make duplicate location-bearing requests because CLI entry points run on import.

Mitigation: Review or guard CLI entry points before deployment, and test request counts with the intended provider configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uynewnas/skills/map-query)
- [AMap API](https://lbs.amap.com/)
- [Baidu Maps API](https://lbsyun.baidu.com/)
- [Tencent Maps API](https://lbs.qq.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance and recommendations with optional shell commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires at least one configured map provider API key; results depend on third-party provider data, quotas, and address accuracy.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package.json and SKILL.md list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
