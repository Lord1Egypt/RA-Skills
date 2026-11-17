## Description:

Pollen Monitor queries China Weather Network pollen concentration levels and protection advice for supported mainland China cities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noviarick](https://clawhub.ai/user/noviarick)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up recent and forecast pollen levels for supported mainland China cities and summarize practical exposure guidance.

### Deployment Geography for Use:

Global, with pollen data coverage limited to supported mainland China cities.

## Known Risks and Mitigations:

Risk: Queries send the selected city and date range to an external weather data service.

Mitigation: Use only with queries that are appropriate to share with that service, and review network access expectations before deployment.

Risk: The skill is limited to supported mainland China cities and may return no data or delayed forecast information.

Mitigation: Confirm the city is on the supported list and treat forecasts as informational rather than guaranteed real-time conditions.

Risk: Pollen protection advice may be incomplete for a user's medical situation.

Mitigation: Use the report for general awareness and rely on clinical or official public health guidance for medical decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/noviarick/skills/pollen-monitor)
- [China Weather Network Pollen Channel](https://m.weather.com.cn/huafen/)
- [Supported City List](https://m.weather.com.cn/huafen/cityChoose.html)
- [Pollen Data Endpoint](https://graph.weatherdt.com/ty/pollen/v2/hfindex.html)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text report with command-line invocation examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and python3; Bash helper also requires jq.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
