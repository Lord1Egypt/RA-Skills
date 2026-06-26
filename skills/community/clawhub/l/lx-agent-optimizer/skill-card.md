## Description: <br>
LX Agent Optimizer helps agents learn from prior mistakes, act proactively, keep cron workflows disciplined, control token cost, and reduce false positives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paoloxiamn](https://clawhub.ai/user/paoloxiamn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit and tune agent behavior, memory, cron jobs, proactive notifications, and token usage so recurring workflows become cheaper and less noisy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages proactive reads, memory or log updates, calendar or channel checks, and workspace changes that may expose private context or create unwanted persistent changes. <br>
Mitigation: Review cron jobs, memory writes, local-file access, and repository changes before use; require confirmation for commits, private-data access, external probes, and persistent memory or TOOLS.md updates. <br>
Risk: Some examples are tailored to Paolo-specific paths and environment assumptions. <br>
Mitigation: Replace those paths and schedules with scoped configuration for the target environment before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paoloxiamn/lx-agent-optimizer) <br>
- [Behavior Learning](references/behavior-learning.md) <br>
- [Proactive Patterns](references/proactive-patterns.md) <br>
- [Cron Discipline](references/cron-discipline.md) <br>
- [Cost Control](references/cost-control.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file-path and cron-configuration recommendations that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata; artifact frontmatter says 1.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
