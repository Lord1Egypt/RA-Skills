## Description: <br>
Book group flights, team travel tickets and corporate group booking with 10+ passenger discounts and bulk fare deals. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and travel coordinators use this skill to search real-time group flight options for organizations or groups that need 10 or more seats on the same route. It helps collect route parameters, run flyai CLI searches, apply fallback searches, and return concise booking-oriented Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install or ask the user to install a global flyai CLI package, including a sudo fallback. <br>
Mitigation: Install the CLI manually only after independently trusting the package source, and avoid automated global or sudo installation in managed environments. <br>
Risk: Travel queries may include sensitive passenger, passport, or business travel details and the artifact describes optional raw query logging. <br>
Mitigation: Avoid entering sensitive traveler data unless logging is disabled or controlled, and limit logs to non-sensitive execution metadata where possible. <br>
Risk: Flight availability and pricing can be wrong if an agent answers from memory or omits validated booking links. <br>
Mitigation: Require fresh flyai CLI results and include only entries with detailUrl-based booking links. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/dingtom336-gif/group-flights) <br>
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for live travel data; should not return raw JSON or fabricate flight prices, flight numbers, or booking links.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
