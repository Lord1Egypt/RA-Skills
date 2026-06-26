## Description: <br>
Searches international flights from China to worldwide destinations and pairs flight results with visa, entry policy, transit, and document guidance from the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to search China-origin international flights, compare route options, and surface visa or transit requirements alongside booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install and run a third-party global travel CLI, and fallback instructions may suggest sudo installation. <br>
Mitigation: Require explicit user approval before installation, avoid automatic sudo or global installs where possible, and run the CLI only in trusted environments. <br>
Risk: Travel and visa queries may be sent to the provider and raw requests may be written to a local .flyai-execution-log.json file. <br>
Mitigation: Share only necessary travel details, review provider handling expectations, and avoid or delete the local execution log when raw request retention is not desired. <br>


## Reference(s): <br>
- [Parameter and output templates](references/templates.md) <br>
- [International flights playbooks](references/playbooks.md) <br>
- [Failure recovery fallbacks](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with comparison tables, booking links, and concise CLI failure guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for live prices, routes, visa information, and booking links.] <br>

## Skill Version(s): <br>
v3.2.4 (source: ClawHub release evidence; artifact frontmatter says 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
