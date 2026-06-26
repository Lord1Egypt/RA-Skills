## Description: <br>
Complete weather system powered by Open-Meteo for global city weather lookup and scheduled weather subscriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zykkk-power](https://clawhub.ai/user/zykkk-power) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to look up current or forecast weather for global cities and manage scheduled weather deliveries in OpenClaw-supported channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled subscription and timezone data may contain stale or unintended delivery targets. <br>
Mitigation: Review or clear data/subscriptions.json and data/user_timezones.json before creating or running subscriptions. <br>
Risk: Scheduled weather pushes can send messages to recipients or channels the user does not control. <br>
Mitigation: Create subscriptions only for controlled targets and confirm the timezone, city, schedule, and delivery target before enabling delivery. <br>
Risk: Weather reports and lifestyle advice depend on Open-Meteo and geocoding results, which may be unavailable or inaccurate. <br>
Mitigation: Treat reports as informational, rerun lookups when freshness matters, and verify high-impact decisions with an authoritative weather source. <br>


## Reference(s): <br>
- [Open-Meteo](https://open-meteo.com/) <br>
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown weather bulletins, JSON subscription records, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Weather reports are formatted in Chinese; subscription flows store delivery and timezone state.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
