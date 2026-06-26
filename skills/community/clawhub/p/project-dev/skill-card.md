## Description: <br>
Coordinates frontend and backend developer agents on managed software projects, including task pickup, project workflow, branch and PR standards, QA handoff, escalation, and heartbeat queue checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developer agents and agent operators use this skill to keep frontend or backend implementation work aligned with project plans, task boards, pull request expectations, QA handoff, and escalation paths. It is intended for managed OpenClaw project teams that rely on separate Git and task-management skills for external operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended heartbeat queue checks and task pickup can trigger unintended work, credit spend, or exposure of sensitive project context if configured too broadly. <br>
Mitigation: Enable heartbeat only with strict project and task filters, spending limits, scoped access, and manual review for unfamiliar tasks; keep credentials, customer data, and sensitive business context out of task fields. <br>
Risk: The skill depends on separate Git and task-management skills that may hold API credentials and perform external operations. <br>
Mitigation: Install only the required dependency skills, keep API keys local to those skills, and scope Git and task-board access to the specific repositories and projects the agent role needs. <br>


## Reference(s): <br>
- [Task Workflow](references/task_workflow.md) <br>
- [Git Workflow](references/git_workflow.md) <br>
- [PR and QA Handoff](references/pr_and_qa_handoff.md) <br>
- [Escalation to Engineer](references/escalation_to_engineer.md) <br>
- [Asana Standards](references/asana_standards.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with task comments, PR templates, branch and commit conventions, escalation formats, and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires separately installed Git and task-management skills for repository and board operations; this skill provides workflow instructions only.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
