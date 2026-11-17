## Description: <br>
A basic multi-agent development workflow that decomposes implementation plans, dispatches fresh subagents for each task, and applies staged specification and code-quality reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to execute clear multi-task implementation plans with isolated subagent context, tracked task progress, and staged review loops for specification fit and code quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read repository files, run development commands, edit code, and create commits. <br>
Mitigation: Use it only in repositories where that level of agent access is acceptable, and review plans and outputs before applying changes. <br>
Risk: Sensitive workspace contents or secrets could be exposed to the agent workflow. <br>
Mitigation: Remove secrets from the workspace or use a sanitized development environment before invoking the skill. <br>
Risk: Serial subagent execution and repeated review loops can increase time and model cost. <br>
Mitigation: Use clear, bounded implementation plans and split ambiguous work into smaller tasks before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/multi-agent-dev-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with task lists, review findings, code changes, shell commands, and optional JSON-style execution summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an agent platform that can read files, run development commands, edit code, and dispatch subagents.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.json release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
