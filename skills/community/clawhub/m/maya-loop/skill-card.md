## Description:

Maya Loop provides a six-step AI-assisted engineering workflow and a five-ring autonomous operations framework for multi-agent development, review, monitoring, and recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason989303](https://clawhub.ai/user/jason989303)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to structure code changes, deployment work, verification, backup, audit logging, and multi-agent review loops. It is intended for controlled engineering workflows that need explicit scoping, checkpoints, and operational records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes broad automatic operational behavior, including deployment, service-control, scheduled automation, backup, memory, and cloud-transfer workflows.

Mitigation: Use only in a tightly controlled engineering environment and require explicit approval before service control, deployment, cloud transfer, or scheduled automation.

Risk: Global memory writes and backups can persist sensitive or irrelevant project data if destinations and filters are not defined.

Mitigation: Disable global memory writes until reviewed, define backup destinations, and add secret filtering before installation.

Risk: Hard-coded approvers, routes, or automation triggers may not match the installing team's authority model.

Mitigation: Replace hard-coded approvers and routing values with environment-specific reviewers, escalation paths, and activation rules before use.

## Reference(s):

- [Server-resolved source repository](https://github.com/Jason989303/maya-loop)
- [Server-resolved source commit](https://github.com/Jason989303/maya-loop/commit/48e7ea4f2baa5b42503857067387d72fe54ef7f7)
- [ClawHub skill page](https://clawhub.ai/jason989303/skills/maya-loop)
- [Publisher profile](https://clawhub.ai/user/jason989303)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, tables, and inline command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agent workflow decisions, verification steps, backup practices, audit logging, service automation, and review behavior.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
