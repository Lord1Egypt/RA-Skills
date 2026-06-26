## Description: <br>
Search for last available seats on nearly full flights, with support for flight booking, hotel reservations, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel tasks powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-focused agents use this skill to collect route details, execute flyai travel-search commands, and present current booking options with booking links. It is intended for urgent or constrained travel searches where the user needs last-seat, cheapest, fastest, direct, or nearby fallback options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask the agent to install the FlyAI CLI globally with npm. <br>
Mitigation: Review and approve the exact npm install command before execution, and confirm Node.js and npm are expected in the environment. <br>
Risk: The skill can run flyai travel-search commands and return booking links that may lead to purchases. <br>
Mitigation: Review each generated command before approval and inspect booking links, prices, dates, and routes before making a purchase. <br>
Risk: Travel results may be misleading if the agent answers from model knowledge instead of live CLI output. <br>
Mitigation: Require results to come from flyai CLI output and omit any result that lacks a detailUrl-backed booking link. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/last-seat-flight) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with travel result tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel results and includes a Powered by flyai brand tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
