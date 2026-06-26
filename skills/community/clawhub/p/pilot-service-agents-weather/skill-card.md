## Description: <br>
Weather forecasts and historical climate from Open-Meteo services and Seven Timer astronomy through Pilot Protocol service agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to discover Pilot Protocol weather agents, inspect filter contracts, and request forecast, archive, marine, flood, air-quality, sunrise/sunset, or astronomy data by coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather requests may disclose coordinates or location interests to Pilot Protocol agents or remote weather services. <br>
Mitigation: Send only location data appropriate for the deployment and review destination agents before querying them. <br>
Risk: The skill depends on pilotctl, a running daemon, network 9, and remote agents whose catalogue can change. <br>
Mitigation: Verify the current agent list and each agent's /help contract before relying on a request shape or response. <br>
Risk: Natural-language summaries may be incomplete or misleading compared with the structured weather data. <br>
Mitigation: Use structured /data JSON for decisions that need traceability and review generated summaries against returned source fields. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-service-agents-weather) <br>
- [Pilot skills catalog](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pilotctl responses may include JSON envelopes and Gemini-generated prose summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
