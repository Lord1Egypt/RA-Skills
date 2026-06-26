## Description: <br>
Fly to mountains, search ski resort flights and highland city flights with alpine destination booking. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more -- powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to search mountain, ski resort, and highland-city flights with real-time booking links from the flyai CLI. It guides parameter collection, fallback searches, and Markdown presentation for mountain travel itineraries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install a global third-party travel CLI. <br>
Mitigation: Require explicit approval before installing @fly-ai/flyai-cli and verify the package source in the local environment. <br>
Risk: Travel searches and optional execution logs may include sensitive itinerary details. <br>
Mitigation: Avoid entering highly sensitive identity or visa details, and review or delete .flyai-execution-log.json if it is created. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/mountain-flight) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight listings must be sourced from flyai CLI output and include detailUrl booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
