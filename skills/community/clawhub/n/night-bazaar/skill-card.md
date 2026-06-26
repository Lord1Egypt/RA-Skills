## Description: <br>
Find night markets, food streets, and local culinary hotspots, with additional travel lookup support for flights, hotels, train tickets, attractions, itinerary planning, visa information, travel insurance, car rental, and related Fliggy-powered services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to retrieve real-time night-market, street-food, attraction, and travel booking options through the flyai CLI, then present concise Markdown results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and execute a global third-party flyai CLI. <br>
Mitigation: Review the CLI package before installation, install it manually when possible, and require confirmation before running npm installs or shell commands. <br>
Risk: Travel queries and command execution details may be written to .flyai-execution-log.json. <br>
Mitigation: Avoid entering passport, payment, or booking-reference details, and delete or disable the local execution log when query retention is not desired. <br>
Risk: The skill returns booking links and can route users toward purchases. <br>
Mitigation: Review destination links before booking and keep final purchase decisions under explicit user control. <br>


## Reference(s): <br>
- [Parameter and Output Templates](references/templates.md) <br>
- [Night Market Playbooks](references/playbooks.md) <br>
- [Fallback Procedures](references/fallbacks.md) <br>
- [Execution Log Runbook](references/runbook.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/night-bazaar) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when setup or recovery is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should be based on flyai CLI output and include a booking link for each listed item when results are available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
