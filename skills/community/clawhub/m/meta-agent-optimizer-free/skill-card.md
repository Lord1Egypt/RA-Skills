## Description: <br>
Records AI agent learnings, errors, and feature requests as structured logs so corrections and failures can become reusable project knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical leads, product managers, and teams use this skill to maintain Markdown learning logs for agent corrections, command failures, feature requests, recurrence checks, and promotion of stable project rules into agent guidance files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation context, raw errors, parameters, and project rules into repository files. <br>
Mitigation: Review each write before keeping it, redact tokens and private data from logs, and keep .learnings local or gitignored by default unless the team has approved sharing. <br>
Risk: Promoting logged observations into agent guidance files can make incorrect or overly specific rules influence future work. <br>
Mitigation: Manually review promoted entries for accuracy, scope, and relevance before adding them to CLAUDE.md, AGENTS.md, or similar project memory files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and structured log templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates local .learnings Markdown files and may propose promotion of reusable rules into CLAUDE.md, AGENTS.md, or related project guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
