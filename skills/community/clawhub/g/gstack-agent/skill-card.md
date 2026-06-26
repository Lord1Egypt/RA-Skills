## Description: <br>
GStack Agent provides a role-based software delivery workflow for product planning, architecture review, design, coding, testing, release, monitoring, documentation, and retrospectives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rocbond](https://clawhub.ai/user/rocbond) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill to route common software delivery tasks to specialized agent roles, including product review, engineering review, code review, QA, release preparation, deployment, monitoring, and documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit code from broad prompts. <br>
Mitigation: Install it only in repositories where agent file writes are acceptable, and use `/qa-only` when report-only testing is needed. <br>
Risk: Release workflows may push branches, merge PRs, deploy, or revert production changes. <br>
Mitigation: Require explicit manual approval before rebases, pushes, PR merges, deployments, or production reverts. <br>
Risk: The artifact includes guard and freeze modes, but sensitive work still depends on users enabling them. <br>
Mitigation: Use `/guard` or `/freeze` before high-risk work, especially production fixes or scoped edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rocbond/gstack-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with reports, plans, code edits, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include proposed or applied repository changes depending on the invoked role and user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
