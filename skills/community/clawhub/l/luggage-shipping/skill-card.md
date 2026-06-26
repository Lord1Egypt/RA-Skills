## Description: <br>
Searches flight options with luggage shipping and extra baggage transport using the flyai CLI and Fliggy service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bufferstreamer](https://clawhub.ai/user/bufferstreamer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to search live flight options where luggage shipping, baggage delivery, or extra baggage transport matters. It collects route/date constraints, runs the flyai CLI, and returns bookable options with comparison tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and run an unpinned global npm package before answering travel queries. <br>
Mitigation: Require manual approval for installation, prefer a reviewed pinned version of @fly-ai/flyai-cli, and run commands in a constrained environment. <br>
Risk: Route, date, budget, and other travel details may be sent to the external flyai or Fliggy service. <br>
Mitigation: Limit personal travel details to what is needed for the search and confirm that external service use is acceptable before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bufferstreamer/luggage-shipping) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands when execution is required] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight results must be based on flyai CLI output, include booking links from detailUrl, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
