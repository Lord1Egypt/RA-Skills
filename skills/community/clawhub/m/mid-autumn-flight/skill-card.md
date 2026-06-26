## Description: <br>
Book Mid-Autumn Festival flights for moon festival travel and autumn reunion. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to collect route details, run flyai CLI flight searches, and present Mid-Autumn Festival booking options with source booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run local commands and install an unpinned global npm CLI before use. <br>
Mitigation: Install or run @fly-ai/flyai-cli only in a controlled environment after user approval, and avoid allowing the skill to perform the global install automatically. <br>
Risk: Flight and booking outputs may direct users to external booking pages where personal or payment information is entered. <br>
Mitigation: Verify each booking link and provider details before sharing personal or payment information. <br>


## Reference(s): <br>
- [Parameter collection and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Failure recovery](references/fallbacks.md) <br>
- [Execution runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown flight summaries with comparison tables, booking links, and inline shell commands when setup or execution is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai CLI output as the required source for travel options; every listed result is expected to include a booking link.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
