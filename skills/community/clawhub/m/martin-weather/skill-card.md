## Description: <br>
Get current weather and forecasts with no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to fetch current weather, compact weather summaries, forecasts, and programmatic weather JSON from public weather services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups send city names, airport codes, or coordinates to public weather services. <br>
Mitigation: Prefer city-level locations over exact home or sensitive coordinates when privacy matters. <br>


## Reference(s): <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo forecast API documentation](https://open-meteo.com/en/docs) <br>
- [ClawHub skill page](https://clawhub.ai/godferylindsay/martin-weather) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; sends queried locations or coordinates to wttr.in or Open-Meteo.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
