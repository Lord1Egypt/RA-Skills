## Description:

Project Developer guides developer agents through task pickup, Git workflow, task-board communication, engineer escalation, PR handoff, QA feedback, and heartbeat queue checks for managed software projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developer agents use this skill to operate as frontend or backend team members on managed software projects. It helps them follow project phase gates, pick up assigned tasks, coordinate through task boards and queue files, escalate blockers, prepare PRs, and hand work to QA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent could update the wrong branch, queue, or board column if project metadata is stale or misread.

Mitigation: Review branch naming, escalation-channel, HEARTBEAT.md write-back, and task-completion ownership rules before use.

Risk: Dependency skills perform Git and task-manager operations with their own credentials.

Mitigation: Install only for developer agents with appropriately scoped Git and task-manager skills, limited to the repositories and projects required by the agent role.

Risk: Heartbeat failures or self-messaging can waste model cycles or create misleading coordination signals.

Mitigation: Preserve the fail-cheap heartbeat behavior, direct queue lookups, and prohibition on self-sends or retries with primary models.

## Reference(s):

- [Project Developer ClawHub page](https://clawhub.ai/encryptshawn/skills/project-dev)
- [OpenClaw Projects ClawHub page](https://clawhub.ai/encryptshawn/openclaw-projects)
- [Build a Dev Team ClawHub page](https://clawhub.ai/encryptshawn/build-dev-team)
- [Task Workflow](artifact/references/task_workflow.md)
- [Git Workflow](artifact/references/git_workflow.md)
- [PR and QA Handoff](artifact/references/pr_and_qa_handoff.md)
- [Escalation to Engineer](artifact/references/escalation_to_engineer.md)
- [Asana Standards](artifact/references/asana_standards.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline templates and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include branch names, task comments, PR descriptions, queue messages, and API contract snippets.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
