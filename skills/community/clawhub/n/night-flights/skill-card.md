## Description: <br>
Helps agents find overnight and late-night flight departures by collecting route and date parameters, running the flyai CLI, and formatting real-time results with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to search for red-eye or late-night flights, compare options, and present booking-linked Markdown results in the user's language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install and run a global third-party CLI that sends travel search details to an external service. <br>
Mitigation: Review and trust @fly-ai/flyai-cli before installation, run it in an approved environment, and only allow global or sudo installation when intentionally approved. <br>
Risk: Raw travel queries may be retained locally in .flyai-execution-log.json when logging is enabled. <br>
Mitigation: Avoid entering sensitive travel details and delete or disable the local execution log when query retention is not desired. <br>
Risk: Flight prices and availability can become stale or unavailable if the CLI fails. <br>
Mitigation: Require fresh flyai CLI results with booking links and report retrieval failures instead of substituting unsourced travel data. <br>


## Reference(s): <br>
- [Parameter and output templates](references/templates.md) <br>
- [Flight search playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables with booking links and occasional bash commands for flyai installation, search, or retry steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires fresh flyai CLI output for travel data and should not fabricate prices, schedules, or booking links.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
