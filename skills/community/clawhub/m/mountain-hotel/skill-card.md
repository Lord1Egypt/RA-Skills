## Description: <br>
Book flights to mountain hotels and highland resort destinations, with support for flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more, powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to search mountain hotel and highland resort routes with live flyai CLI results. The skill helps collect required route parameters and return Markdown flight options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install the flyai CLI globally. <br>
Mitigation: Use a reviewed or pinned flyai CLI version in an isolated environment, and require confirmation before package installation. <br>
Risk: Travel search details are sent to an external service. <br>
Mitigation: Tell users before external searches and avoid submitting sensitive or unnecessary personal details. <br>
Risk: Flight prices and booking links depend on live CLI output. <br>
Mitigation: Show only results that include detailUrl booking links and disclose CLI failures instead of filling gaps from memory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiejinsong/mountain-hotel) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results and include detailUrl booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
