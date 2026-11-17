## Description:

Run non-time-sensitive compute, research, and batch tasks overnight through a cron-scheduled OpenClaw agent workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willificent](https://clawhub.ai/user/willificent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to queue heavy, non-urgent work for overnight execution when compute capacity may be cheaper or more available. It is suited to batch research, document summarization, model-intensive analysis, and similar tasks that can wait for review the next day.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged script includes preloaded unrelated tasks that can run later under a broadly privileged main agent with access to local context and external accounts.

Mitigation: Inspect and empty the packaged script before installation, remove preloaded tasks, require per-task approval, scope credentials and file access, and record completed tasks so external actions cannot repeat automatically.

Risk: Scheduled tasks run with full user privileges and no sandboxing or credential isolation.

Mitigation: Test each task manually before scheduling, avoid embedding secrets, restrict script permissions to the owner, and review network and file actions before execution.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/willificent/skills/off-peak-compute)
- [Publisher profile](https://clawhub.ai/user/willificent)

## Skill Output:

**Output Type(s):** [markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with bash code blocks and a shell script template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cron setup steps, task queue guidance, and log review commands.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
