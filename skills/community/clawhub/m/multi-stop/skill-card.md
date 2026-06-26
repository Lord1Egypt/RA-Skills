## Description: <br>
Plan complex multi-city flight itineraries from one city to the next, optimizing total cost with live results from the flyai CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to have an agent collect multi-city travel parameters, run flyai CLI searches for each leg, and summarize real-time travel options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an unpinned global flyai npm CLI. <br>
Mitigation: Use an isolated environment, pin the CLI version when possible, avoid sudo installation, and review CLI permissions before running searches. <br>
Risk: Travel-search details are sent to the flyai provider and may include personal itinerary information. <br>
Mitigation: Use the skill only when sharing those trip details with the provider is acceptable, and avoid entering unnecessary sensitive information. <br>
Risk: The artifact may persist raw travel queries locally in .flyai-execution-log.json. <br>
Mitigation: Disable, remove, or protect the local execution log when raw travel queries should not be retained. <br>
Risk: Booking links and prices come from third-party CLI output. <br>
Mitigation: Verify fares, itinerary details, and destination URLs before purchase, and do not rely on results that lack live CLI booking links. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiejinsong/multi-stop) <br>
- [README](README.md) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Failure fallbacks](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown travel-search summaries with comparison tables and booking links, backed by flyai CLI commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI output; responses should include booking links from CLI data and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
