## Description: <br>
Book National Day holiday flights for October 1st Golden Week travel, with support for flight booking, hotel reservations, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel tasks powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search and compare National Day and Golden Week travel options, especially flights, using flyai CLI results rather than model memory. It helps collect route and date parameters, run the correct travel search command, and format booking-ready Markdown with links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prompt an agent to install and use an external global travel CLI. <br>
Mitigation: Review and install @fly-ai/flyai-cli manually before use, or approve the install only in a controlled environment. <br>
Risk: Broad travel wording may activate the skill when the user intent is not a specific flight search. <br>
Mitigation: Use it for clear National Day, Golden Week, or flight-booking requests and confirm route, date, filters, and booking links before acting. <br>
Risk: Travel availability and pricing can change quickly or be incorrect if not taken from live CLI output. <br>
Mitigation: Require flyai CLI execution and include only results that provide detailUrl booking links. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/national-day-flight) <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs must be based on flyai CLI results and include booking links for listed options.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
