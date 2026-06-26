## Description: <br>
Get current weather and forecasts without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gooduone](https://clawhub.ai/user/gooduone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up current weather and forecasts from public weather services using curl, including quick text forecasts and JSON fallback data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries are sent to public third-party services, which can observe the requested location and network metadata. <br>
Mitigation: Use only non-sensitive locations and review outbound curl requests before execution. <br>
Risk: Forecasts and current conditions depend on external service availability and accuracy. <br>
Mitigation: Treat results as informational and verify important weather decisions with an authoritative source. <br>


## Reference(s): <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo forecast API documentation](https://open-meteo.com/en/docs) <br>
- [ClawHub skill page](https://clawhub.ai/gooduone/gooduone-test-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and service response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and makes outbound requests to public weather services.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
