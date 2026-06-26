## Description: <br>
Book flights for golf trips to world-class golf resorts and courses, with related travel-planning support powered by Fliggy and flyai CLI output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search live flyai flight options for golf trips, compare recommended, cheapest, fastest, direct, or flexible-date routes, and return Markdown results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger on broad planning language and route travel details to the flyai provider. <br>
Mitigation: Use it only for explicit golf-trip or flight-search requests, and confirm the user is comfortable sharing origin, destination, dates, and preferences with the travel provider. <br>
Risk: The skill instructs agents to install an unpinned global npm CLI package automatically. <br>
Mitigation: Require explicit approval before installation, pin or pre-approve a trusted @fly-ai/flyai-cli version, and prefer an isolated environment. <br>
Risk: Flight results may be stale, malformed, or unavailable if the live CLI call fails. <br>
Mitigation: Return only data from successful flyai CLI output with detailUrl booking links, retry once on transient failure, and avoid fabricating fallback travel options. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/dingtom336-gif/golf-trip) <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI data and booking detailUrl links; raw JSON output is disallowed by the skill instructions.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
