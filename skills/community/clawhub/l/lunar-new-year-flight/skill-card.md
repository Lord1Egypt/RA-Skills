## Description: <br>
Book Lunar New Year flights for Spring Festival reunion and Chinese New Year travel, using FlyAI CLI results for real-time Fliggy-powered booking options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bufferstreamer](https://clawhub.ai/user/bufferstreamer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to search Lunar New Year and Spring Festival flights, compare recommended, cheapest, fastest, or direct options, and return booking-ready Markdown results with links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and run a global third-party FlyAI CLI. <br>
Mitigation: Require explicit user approval before installation or CLI execution, verify the CLI source and version, and avoid using the skill in environments where global npm installs are not allowed. <br>
Risk: Booking workflows can expose users to external purchase links. <br>
Mitigation: Confirm route, date, and traveler intent before presenting or following booking links, and make clear that prices and availability come from live CLI output. <br>


## Reference(s): <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight results must come from FlyAI CLI output and include booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
