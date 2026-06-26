## Description: <br>
Book flights for photography trips to scenic destinations, with support for related travel planning tasks powered by Fliggy and flyai CLI output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivan97](https://clawhub.ai/user/ivan97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search flight options for photography-focused trips, compare recommended, cheapest, fastest, or direct routes, and return bookable results from flyai CLI output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically install and run an unpinned global npm CLI. <br>
Mitigation: Require manual approval for installation or use a pinned, sandboxed install of @fly-ai/flyai-cli before execution. <br>
Risk: Broad travel requests may trigger flight-search commands beyond the user's intended scope. <br>
Mitigation: Confirm required route and date parameters before execution and limit commands to the documented flyai parameters. <br>
Risk: Flight results could be misleading if generated without live CLI data. <br>
Mitigation: Only return results sourced from flyai CLI output and omit any option that lacks a Book link. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivan97/photography-trip) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown flight-search results with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output; every listed result must include a Book link.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
