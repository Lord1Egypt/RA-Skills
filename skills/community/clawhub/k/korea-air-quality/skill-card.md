## Description: <br>
Korea Air Quality helps agents answer South Korea air-quality requests, resolve Korean region names or saved locations, compare regions, and prepare local alerts or morning briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twbeatles](https://clawhub.ai/user/twbeatles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to answer Korean air-quality questions, store default regions or coordinates, compare multiple locations, and draft alert or morning-briefing automation for South Korea. <br>

### Deployment Geography for Use: <br>
South Korea <br>

## Known Risks and Mitigations: <br>
Risk: Local state files can retain saved regions, exact coordinates, alert rules, alert history, station cache, and provider settings. <br>
Mitigation: Avoid saving precise coordinates unless needed and review or delete local data files when location history should not be retained. <br>
Risk: An AirKorea API key may be stored in data/config.json if configured that way. <br>
Mitigation: Prefer supplying AIRKOREA_API_KEY from the environment instead of storing the key in a local config file. <br>
Risk: Generated cron plans may include a hard-coded local path. <br>
Mitigation: Review and adjust each generated cron plan before installing or running it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twbeatles/korea-air-quality) <br>
- [API and Product Plan](references/api-and-product-plan.md) <br>
- [Alert and Morning Briefing](references/alert-and-briefing.md) <br>
- [Domestic API Notes](references/domestic-api-notes.md) <br>
- [Integration Roadmap Status](references/integration-roadmap.md) <br>
- [Location Resolution Strategy](references/location-resolution.md) <br>
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search) <br>
- [Open-Meteo Air Quality API](https://air-quality-api.open-meteo.com/v1/air-quality) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Korean text or Markdown summaries, optional JSON CLI output, and shell command examples for local configuration and automation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local state files under data/ for user preferences, saved coordinates, alert rules, alert history, station cache, and provider configuration.] <br>

## Skill Version(s): <br>
2026.4.16 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
