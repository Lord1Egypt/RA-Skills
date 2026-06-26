## Description: <br>
Plan multi-city flights, 3+ city complex routes and open-jaw itineraries with multi-stop flight booking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to search each leg of multi-city, open-jaw, and stopover flight itineraries with current flyai CLI results and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and rely on the flyai CLI for live travel searches. <br>
Mitigation: Review and install the CLI yourself before use, and only run it if you trust the provider handling itinerary searches. <br>
Risk: The skill may store raw travel requests locally in .flyai-execution-log.json. <br>
Mitigation: Disable or delete the local execution log if raw travel requests should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/multi-city) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Fallback guidance](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown itinerary summaries with inline shell commands and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include leg-by-leg itinerary details, booking links, cost summaries, and connection warnings.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
