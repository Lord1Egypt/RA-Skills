## Description:

Universal debug and deploy expert for multi-project instances, used for service debugging, backend, frontend, and mobile deployment, troubleshooting, CI/CD, testing, error handling, and DevOps tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuanji-ai-2026](https://clawhub.ai/user/xuanji-ai-2026)

### License/Terms of Use:

Dual License (Community Free / Commercial Paid)

## Use Case:

Developers and operations engineers use this skill to guide debugging, deployment, testing, configuration, and incident-response work across backend, frontend, mobile, and infrastructure projects. It emphasizes evidence-based checks, project isolation, and controlled operational procedures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide command execution, file modification, service changes, remote operations, and rollback activity.

Mitigation: Require human approval for remote commands, service changes, firewall changes, deletions, rollbacks, and other production-impacting operations.

Risk: The skill may encounter production credentials or sensitive operational context during debugging and deployment work.

Mitigation: Use only with agent platforms that enforce secret redaction and keep the skill away from production credentials when those controls are not available.

Risk: The skill describes durable state and checkpoints that could become stale or inaccurate.

Mitigation: Treat saved checkpoints as context only and re-check live system state, logs, and command output before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuanji-ai-2026/skills/group-debug-deploy-expert)
- [Publisher profile](https://clawhub.ai/user/xuanji-ai-2026)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline command, code, configuration, and diagnostic guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose high-impact operational actions that require human review before execution.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
