## Description: <br>
Finds military flight benefits, veteran discounts, armed forces travel deals, and related travel options through flyai and Fliggy-sourced results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search for military-friendly flights and related travel services, collect missing trip parameters, run flyai CLI searches, and present bookable Markdown results with military ID reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install a global CLI tool before retrieving travel results. <br>
Mitigation: Review and approve any npm global installation yourself, and confirm the package being installed before execution. <br>
Risk: Travel, visa, identity, or booking details may be entered while using the skill. <br>
Mitigation: Avoid sharing unnecessary personal information and review any CLI output or booking page before acting on it. <br>
Risk: The documented execution log can persist raw travel queries locally when filesystem writes are available. <br>
Mitigation: Check for local execution logs and disable or remove them when they may contain sensitive trip details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/military-flights) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires each flight result to include a booking link sourced from flyai CLI output.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
