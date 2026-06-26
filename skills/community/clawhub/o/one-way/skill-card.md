## Description: <br>
Search one-way flights, single-trip tickets and open-ended travel bookings with no return date required, powered by Fliggy/FlyAI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-assistant agents use this skill to search one-way flights, collect required route and date parameters, execute FlyAI CLI searches, and present bookable real-time results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store raw travel requests and command details in a persistent local execution log. <br>
Mitigation: Review logging behavior before deployment, confirm whether logs can be disabled or deleted, and avoid entering passport, visa, payment, or highly personal itinerary details unless retention is controlled. <br>
Risk: Travel searches are sent through a global FlyAI CLI to an external travel service. <br>
Mitigation: Install and use the CLI only where external travel-service processing is acceptable, and inform users that real-time search data comes from FlyAI/Fliggy. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FlyAI CLI output; user-facing results should include booking links and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
