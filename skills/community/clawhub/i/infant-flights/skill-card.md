## Description: <br>
Book infant flights, baby travel tickets and bassinet seat options with child fare and infant-in-arm booking, with related travel search support powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search infant-friendly flights, direct routes, child-fare travel options, and related booking links through the flyai CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install or require a global flyai CLI before returning travel results. <br>
Mitigation: Review the CLI package before installation and do not allow automatic global or sudo installation unless the environment intentionally trusts that CLI. <br>
Risk: Travel-search details may be sent to FlyAI or Fliggy when the CLI runs. <br>
Mitigation: Use the skill only when the user accepts sharing the required route, date, and travel-search details with the travel provider. <br>
Risk: The skill may retain local raw travel-query history in `.flyai-execution-log.json`. <br>
Mitigation: Check for the log file after use and remove or disable it when local retention of travel-query history is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/infant-flights) <br>
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Failure fallbacks](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, baby travel tips, and inline flyai CLI commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI output for flight data and should not answer travel-search results from model memory.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
