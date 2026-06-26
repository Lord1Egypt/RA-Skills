## Description: <br>
Book flights for marathon and running event trips, with additional support for hotel reservations, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel planning powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bufferstreamer](https://clawhub.ai/user/bufferstreamer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to search real-time marathon and race-day travel options, compare flight results, and produce booking-oriented Markdown responses with links from flyai CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and execute the external @fly-ai/flyai-cli package globally. <br>
Mitigation: Require user approval before installation, verify the package source, and prefer a sandboxed or local installation. <br>
Risk: Route, date, and preference data may be sent to the flyai provider during travel searches. <br>
Mitigation: Avoid entering sensitive personal details unless the user accepts the provider's data handling and booking flow. <br>
Risk: Travel prices, availability, and booking links can change quickly. <br>
Mitigation: Use only fresh CLI results and keep the skill's booking-link validation before presenting options. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bufferstreamer/marathon-trip) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with CLI commands, comparison tables, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight results must come from flyai CLI output and include booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
