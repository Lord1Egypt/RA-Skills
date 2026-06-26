## Description: <br>
Get current weather and forecasts (no API key required). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars82311111](https://clawhub.ai/user/mars82311111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for current weather, compact weather summaries, multi-day forecasts, and programmatic weather data from public no-key services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookup locations or coordinates are sent to public third-party weather services. <br>
Mitigation: Avoid sending sensitive locations; use coarse locations or airport codes when precision is unnecessary. <br>
Risk: Examples without an explicit scheme may not make the transport expectation clear. <br>
Mitigation: Prefer explicit HTTPS URLs for wttr.in and Open-Meteo requests. <br>


## Reference(s): <br>
- [Mars Weather Pro on ClawHub](https://clawhub.ai/mars82311111/mars-weather-pro) <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true) <br>
- [Open-Meteo documentation](https://open-meteo.com/en/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and service URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for command examples; can return plain text, PNG output, or JSON depending on the selected weather service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
