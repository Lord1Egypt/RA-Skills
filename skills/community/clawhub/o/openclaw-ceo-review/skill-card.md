## Description: <br>
CEO-perspective plan review and strategy upgrader supporting expansion, selective expansion, hold-scope, and scope-reduction modes before development work begins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product leads, and technical reviewers use this skill to challenge plans before implementation, compare implementation approaches, map failure modes, and identify observability and test gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews repository history, diffs, TODOs, and project documentation, which may include sensitive local project context. <br>
Mitigation: Use it only in projects where that local context is appropriate for the active agent session, and review generated findings before sharing them outside the project. <br>
Risk: Strategic review output can be incomplete or misleading if treated as approval rather than critique. <br>
Mitigation: Have a human reviewer validate the premise challenges, alternatives, failure modes, observability gaps, and testing recommendations before implementation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with inline shell commands and structured checklist sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces premise challenges, alternatives, failure-mode mapping, observability gaps, edge cases, test coverage notes, and status guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
