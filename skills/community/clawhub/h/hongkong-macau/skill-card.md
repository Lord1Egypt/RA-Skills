## Description: <br>
Plans Hong Kong and Macau travel with flyai-cli commands for flights, hotels, attraction tickets, itineraries, visa information, insurance, car rentals, real-time prices, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and agents use this skill to plan Hong Kong and Macau trips by collecting travel parameters, running flyai CLI searches, and formatting real-time flight, hotel, attraction, and itinerary results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask the agent to install the flyai CLI globally with npm. <br>
Mitigation: Review the CLI before installation, require explicit approval for global installs, and prefer a controlled environment when testing the skill. <br>
Risk: Travel-search details may be sent to FlyAI/Fliggy services and raw queries may be stored locally in an execution log. <br>
Mitigation: Avoid sensitive personal, booking, visa, or contact details unless this data sharing is acceptable, and disable or remove the local execution log when privacy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/hongkong-macau) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel data and expects each displayed result to include a booking link.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
