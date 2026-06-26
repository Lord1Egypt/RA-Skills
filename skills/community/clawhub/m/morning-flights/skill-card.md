## Description: <br>
Find the earliest departing flights of the day, maximize your day at the destination by arriving before noon, and format real-time flyai results with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search for early morning flights, compare real-time options, and present booking-ready Markdown results. It is intended for flight discovery workflows that require live flyai CLI output rather than model knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install and run a third-party flyai CLI, including global npm installation paths. <br>
Mitigation: Have the user install @fly-ai/flyai-cli manually from a trusted source, preferably without elevated privileges, and do not allow agents to run sudo or global npm installs automatically. <br>
Risk: Travel queries and execution details may be stored locally in .flyai-execution-log.json. <br>
Mitigation: Tell users before retaining travel-search details and disable or delete .flyai-execution-log.json when local logging is not wanted. <br>
Risk: Flight prices and availability can be incorrect if the agent answers from model knowledge instead of live service output. <br>
Mitigation: Require flyai CLI results and booking detail links for every listed option; re-run the command or report failure when live data is unavailable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/morning-flights) <br>
- [Fallbacks - Flight Category](references/fallbacks.md) <br>
- [Playbooks - early-flights](references/playbooks.md) <br>
- [Runbook - Execution Log Schema](references/runbook.md) <br>
- [Templates - early-flights](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires real-time flyai CLI output and booking detail links; may append local execution logs when filesystem writes are available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
