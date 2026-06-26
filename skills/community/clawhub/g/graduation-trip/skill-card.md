## Description: <br>
Book flights for graduation trips and post-graduation vacations, with related travel planning support powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search graduation-trip flights with the flyai CLI, compare route options, and return Markdown flight summaries with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prompt an agent to install an unpinned global flyai CLI package, which modifies the user's system environment. <br>
Mitigation: Approve CLI installation explicitly, install in an isolated environment when possible, and verify the package source before use. <br>
Risk: Flight searches send route, date, and travel preference details to a FlyAI/Fliggy-backed external service. <br>
Mitigation: Share only travel details needed for the search and avoid entering sensitive personal data unless the service is acceptable for that use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/graduation-trip) <br>
- [Parameter Collection & Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs must be based on flyai CLI results and include booking links for returned flight options.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
