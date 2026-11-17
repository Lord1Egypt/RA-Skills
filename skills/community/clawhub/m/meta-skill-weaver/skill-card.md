## Description:

Use this skill when orchestrating complex multi-step tasks with task decomposition, event-driven multi-skill collaboration, parallel execution, timeout control, interrupt recovery, metrics, and feedback collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to coordinate complex, long-running work across multiple agent skills. It helps decompose broad tasks, assign work to skills, run steps in parallel where appropriate, track progress, collect metrics and feedback, and resume interrupted workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad orchestration capabilities can invoke file writes, shell commands, and execution workflows beyond a simple single-purpose skill.

Mitigation: Install only when broad orchestration is needed, restrict Write/Bash/Exec authority, and require explicit approval for shell commands and event-handler scripts.

Risk: Feedback and metrics behavior can store task feedback, comments, errors, and operational details locally.

Mitigation: Avoid storing sensitive feedback or task error details unless local retention, filesystem permissions, and access controls are acceptable.

Risk: Server security evidence flags incomplete implementation and version inconsistencies.

Mitigation: Treat the release as requiring review until orchestrator entry points and version discrepancies are resolved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pagoda111king/skills/meta-skill-weaver)
- [ClawHub Skill Documentation](https://clawhub.ai/skills/meta-skill-weaver/docs)
- [ClawHub Skill Issues](https://clawhub.ai/skills/meta-skill-weaver/issues)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured orchestration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task decomposition, skill assignments, workflow status, execution reports, metrics summaries, and feedback summaries.]

## Skill Version(s):

2.5.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
