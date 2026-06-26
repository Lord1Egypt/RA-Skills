## Description: <br>
Find night markets, food streets, and local culinary hotspots using flyai CLI results, then format evening food and booking options for the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to find night markets, food streets, and street-food points of interest for a specified city. It collects the city and optional search filters, runs flyai CLI searches, and returns concise Markdown results with booking links when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs a global npm install of the flyai CLI, which can modify the agent environment. <br>
Mitigation: Install only after trusting the flyai CLI provider, preferably in a controlled environment where the package and permissions can be reviewed. <br>
Risk: The runbook describes persistent local logging of travel queries in .flyai-execution-log.json. <br>
Mitigation: Avoid entering sensitive itinerary, passport, or payment details, and disable or delete the log file when local retention is not acceptable. <br>
Risk: The skill can surface booking links and travel purchase paths. <br>
Mitigation: Require user review and confirmation of all booking details before any purchase or payment step. <br>


## Reference(s): <br>
- [Templates - night-market](references/templates.md) <br>
- [Playbooks - night-market](references/playbooks.md) <br>
- [Fallbacks - Attraction Category](references/fallbacks.md) <br>
- [Runbook - Execution Log Schema](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and short guidance with inline booking links and flyai CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel results; no raw JSON should be shown to users.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
