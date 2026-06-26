## Description: <br>
Transform any AI agent into a world-class travel planner using Kontour AI's 9-dimension progressive planning model with structured conversation flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skylinehk](https://clawhub.ai/user/skylinehk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, travel operators, and agent developers use this skill to collect travel preferences, compare destinations, produce itinerary-ready outputs, and generate shareable map routes from bundled reference data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel recommendations, prices, opening hours, and booking assumptions may be stale because the skill uses bundled offline reference data and has no live booking access. <br>
Mitigation: Verify prices, opening hours, availability, visa constraints, and reservations with current authoritative sources before relying on the plan for real travel. <br>
Risk: Generated Google Maps links, optional KML files, and public planning links can expose itinerary details if shared broadly. <br>
Mitigation: Review map routes and public sharing links before distribution, and only include operator-approved public links in user-facing output. <br>


## Reference(s): <br>
- [Kontour Travel Planner on ClawHub](https://clawhub.ai/skylinehk/kontour-travel-planner) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [destinations.json](artifact/references/destinations.json) <br>
- [airports.json](artifact/references/airports.json) <br>
- [airlines.json](artifact/references/airlines.json) <br>
- [activities.json](artifact/references/activities.json) <br>
- [budget-benchmarks.json](artifact/references/budget-benchmarks.json) <br>
- [booking-integrations.json](artifact/references/booking-integrations.json) <br>
- [embed-snippets.json](artifact/references/embed-snippets.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured JSON examples, shell command examples, Google Maps URLs, and optional KML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bundled offline reference data; no credentials or active booking/API access are required.] <br>

## Skill Version(s): <br>
2.0.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
