## Description: <br>
Fetches Swedish pollen forecasts from Pollenrapporten for mapped locations, including severity levels and optional grass pollen alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lauroBRCWB](https://clawhub.ai/user/lauroBRCWB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users ask an agent for current pollen conditions in Sweden by city or nearby reporting region. The skill returns pollen severity levels, forecast text, and optional grass pollen alerts for allergy planning. <br>

### Deployment Geography for Use: <br>
Sweden <br>

## Known Risks and Mitigations: <br>
Risk: Forecast results depend on a disclosed external API and nearest-region mappings, so data may be unavailable, stale, or less precise for smaller towns. <br>
Mitigation: Check the reported region and date range before relying on the forecast, and retry or consult Pollenrapporten directly if live data is unavailable. <br>
Risk: Grass pollen alerts include medication and exposure suggestions that may be mistaken for medical advice. <br>
Mitigation: Treat alert text as informational allergy-planning guidance and follow clinician, medication-label, or local health advice for medical decisions. <br>


## Reference(s): <br>
- [Pollenrapporten API](https://api.pollenrapporten.se/v1/) <br>
- [Region mappings](references/regions.json) <br>
- [ClawHub skill page](https://clawhub.ai/lauroBRCWB/pollen-rapporten) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text forecast summary with severity labels and optional alert lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a city name; optional --alert mode adds grass pollen guidance. Live results depend on api.pollenrapporten.se availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
