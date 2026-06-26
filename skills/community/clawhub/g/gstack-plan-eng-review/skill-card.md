## Description: <br>
Provides an engineering manager-style review of implementation plans, covering architecture, data flow, diagrams, edge cases, tests, performance, and interactive decision points before coding begins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loocor](https://clawhub.ai/user/loocor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to stress-test plans and design docs before implementation. It helps identify scope issues, architecture risks, missing tests, performance concerns, TODO decisions, and failure modes through structured review and one-issue-at-a-time questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect local repository context and Git/GitHub metadata during review. <br>
Mitigation: Use it in repositories where that inspection is acceptable, and review any proposed shell commands before execution. <br>
Risk: The skill may create a test-plan Markdown file under ./test-plans. <br>
Mitigation: Ask for an in-chat-only review when file creation is not desired, or review the generated test-plan file before committing it. <br>
Risk: Opinionated plan-review guidance can be incomplete or misleading when the design doc, branch state, or project context is stale or missing. <br>
Mitigation: Provide the current plan and relevant design docs, then verify recommendations against project constraints before implementation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/loocor/gstack-plan-eng-review) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown review guidance with ASCII diagrams, option prompts, shell command snippets, and a test-plan Markdown file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local repository context and Git/GitHub metadata, and may write a bounded test-plan Markdown file under ./test-plans unless the user asks for an in-chat-only review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
