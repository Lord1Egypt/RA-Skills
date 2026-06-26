## Description: <br>
Plans and compares multi-destination trips across multi-city, open-jaw, round-trip, and single-segment options, optimizes city order, and produces standardized HTML itinerary reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danshaniusha](https://clawhub.ai/user/danshaniusha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travel planners and agents use this skill to compare multi-city routes, transportation modes, prices, schedules, budgets, and itinerary options, then generate a shareable HTML travel-planning report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted itinerary text could cause unintended local command execution through shell-string handling in the bundled scripts. <br>
Mitigation: Run only with trusted itinerary input, review before installation, and prefer a fixed version that uses spawn or execFile argument arrays plus strict city and date validation. <br>
Risk: Bundled HTML examples and live travel searches may show stale or unavailable prices, schedules, or booking options. <br>
Mitigation: Treat generated reports as planning aids, verify current prices and availability with the travel provider before booking, and regenerate reports close to the purchase time. <br>
Risk: Use of the external FlyAI service and optional API key can expose trip details to that service. <br>
Mitigation: Avoid sensitive itinerary text when possible, configure only necessary credentials, and follow local credential-handling policies for FLYAI_API_KEY. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/danshaniusha/multi-city-planner) <br>
- [FlyAI Homepage](https://open.fly.ai/) <br>
- [Usage Guide](references/usage.md) <br>
- [FlyAI Flight Search Reference](skills/flyai/references/search-flight.md) <br>
- [FlyAI Hotel Search Reference](skills/flyai/references/search-hotel.md) <br>
- [FlyAI POI Search Reference](skills/flyai/references/search-poi.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, HTML, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries and generated HTML reports with comparison tables, route details, budgets, checklists, and travel notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and flyai-cli; travel prices and availability are time-sensitive and may depend on an external FlyAI service or optional API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
