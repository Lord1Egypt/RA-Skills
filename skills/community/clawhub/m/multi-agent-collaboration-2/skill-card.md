## Description: <br>
Helps users structure human-in-the-loop multi-agent workflows for product development, content production, code changes, MVP iteration, and other complex deliverables by separating owner direction, orchestration, execution, review, and acceptance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allin-zhang](https://clawhub.ai/user/allin-zhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, product managers, independent builders, small teams, and creators use this skill to turn ambiguous goals into bounded, reviewable tasks for one or more AI agents. It is intended for supervised collaboration where humans confirm plans, review outputs, and perform final acceptance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsupervised or loosely scoped agent execution can expand task scope or produce changes that are difficult to review. <br>
Mitigation: Keep task boundaries explicit, require human confirmation before execution, and review agent outputs before accepting changes. <br>
Risk: Reusable task or review templates can accidentally expose secrets, private paths, or internal project details. <br>
Mitigation: Remove secrets and private internal details before turning project-specific notes into reusable public templates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allin-zhang/multi-agent-collaboration-2) <br>
- [Atomic task template](references/task-template.md) <br>
- [Review checklist](references/review-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Structured Markdown, tables, and task templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is Chinese and emphasizes concise, reviewable task instructions and review summaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
