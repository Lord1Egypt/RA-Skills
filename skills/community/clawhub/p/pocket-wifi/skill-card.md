## Description: <br>
Rent portable WiFi devices for overseas travel - share with travel companions, unlimited data, and pickup/return at airport counters. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to search for portable WiFi rentals and related travel booking options through flyai CLI results, then present concise Markdown recommendations with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install and run a global third-party CLI. <br>
Mitigation: Have the user explicitly approve any @fly-ai/flyai-cli installation before use. <br>
Risk: Travel queries may include sensitive booking, account, passport, or payment data. <br>
Mitigation: Avoid providing passport, payment, account, or other sensitive booking data to the skill. <br>
Risk: The skill can persist raw travel queries in a local .flyai-execution-log.json file. <br>
Mitigation: Disable or remove .flyai-execution-log.json when local query history retention is not desired. <br>


## Reference(s): <br>
- [Parameter SOP and Output Templates](references/templates.md) <br>
- [Pocket Wifi Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Execution Log Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output; booking results must include detailUrl links.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
