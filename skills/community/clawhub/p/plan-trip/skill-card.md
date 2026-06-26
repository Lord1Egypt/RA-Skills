## Description: <br>
Plan your entire trip with AI - flights, hotels, attractions, day-by-day itinerary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to collect trip details, run live travel searches through the flyai CLI, and produce day-by-day plans with flights, hotels, attractions, and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install the flyai CLI globally before running live searches. <br>
Mitigation: Review and approve the global CLI installation before use, or install and verify the CLI in a controlled environment first. <br>
Risk: Travel details are sent to the travel provider for live flight, hotel, attraction, and booking searches. <br>
Mitigation: Avoid entering sensitive travel details unless provider sharing is acceptable for the intended user and deployment. <br>
Risk: Raw trip requests and command history may be retained locally in .flyai-execution-log.json. <br>
Mitigation: Disable, restrict, or delete the local log when request retention is not appropriate. <br>


## Reference(s): <br>
- [Parameter and output templates](references/templates.md) <br>
- [Trip-planning playbooks](references/playbooks.md) <br>
- [Fallback handling](references/fallbacks.md) <br>
- [Execution log schema](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands when retry steps are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI output for travel data and includes booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
