## Description: <br>
Queries pollen concentration levels and health protection guidance for supported mainland China cities using China Weather Network pollen data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NoviaRick](https://clawhub.ai/user/NoviaRick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check current and forecast pollen levels for supported mainland China cities and receive allergy protection guidance. <br>

### Deployment Geography for Use: <br>
Global use; data coverage is limited to supported mainland China cities. <br>

## Known Risks and Mitigations: <br>
Risk: Queries send the requested city and date range to the documented weather-data endpoint. <br>
Mitigation: Use the skill only when that outbound request is acceptable, and avoid entering sensitive information as city arguments. <br>
Risk: The optional Bash helper depends on jq and may fail where jq is unavailable. <br>
Mitigation: Prefer the Python helper unless jq is installed in the runtime environment. <br>


## Reference(s): <br>
- [Pollen Monitor on ClawHub](https://clawhub.ai/NoviaRick/pollen-monitor) <br>
- [China Weather Network Pollen Channel](https://m.weather.com.cn/huafen/) <br>
- [Supported City List](https://m.weather.com.cn/huafen/cityChoose.html) <br>
- [Pollen Data Endpoint](https://graph.weatherdt.com/ty/pollen/v2/hfindex.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text with pollen levels, dates, forecast status, and health guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and python3; the optional Bash helper also requires jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
