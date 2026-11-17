## Description:

Finch mines session history for learning signals, compacts memory, and routes findings back into skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Finch to identify corrections, directives, breakthroughs, and recurring operational issues from agent activity, then route them into memory updates, skill patches, reference files, task lists, or review queues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring access to private operational signals can expose sensitive workspace data.

Mitigation: Install only for environments where always-on self-improvement is intended, limit workspace credential scope, and keep cron or hook loading disabled until permissions are reviewed.

Risk: Automatic repository publishing instructions can push unwanted changes, including force-pushes.

Mitigation: Remove or constrain automatic push and force-push behavior, and require review before repository changes are published.

Risk: The skill can mutate memory, skills, task lists, reference files, and repositories.

Mitigation: Use staged patch routing, review diffs before production changes, and retain rollback artifacts for memory or task-list updates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/indigokarasu/skills/ocas-finch)
- [README](README.md)
- [Scan and Work Architecture](references/scan-work-architecture.md)
- [Mining Methodology](references/mining_methodology.md)
- [Memory and Storage Layout](references/storage-layout.md)
- [Security Architecture](references/security_architecture.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and structured task recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or stage memory, skill, reference, task-list, and repository updates for review or execution by the agent.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
