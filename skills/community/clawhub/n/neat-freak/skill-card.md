## Description:

End-of-session knowledge cleanup that reconciles project docs, root agent guidance, and agent memory against the code, while auditing workspace governance rules for stale references and compliance drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkkkhazix](https://clawhub.ai/user/kkkkhazix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill at project milestones or handoff points to keep README, docs, CLAUDE.md/AGENTS.md, and supported agent memory in sync with the current codebase. It is also used to identify stale rules, dead references, documentation bloat, and governance drift before the next agent or teammate resumes work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect global agent state and persistent configuration beyond the current project if scope is not constrained.

Mitigation: Limit the run to the current project unless broader inspection is explicitly intended.

Risk: The workflow can modify AGENTS.md, CLAUDE.md, memory files, or delete skill directories as part of cleanup.

Mitigation: Require a path-by-path diff and explicit confirmation before persistent agent files are edited or skill directories are deleted.

## Reference(s):

- [Agent memory and configuration paths](references/agent-paths.md)
- [Governance audit details](references/governance.md)
- [Change impact matrix](references/sync-matrix.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown summaries with proposed or applied file edits and shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect or update project documentation, root agent guidance files, and persistent agent memory/configuration depending on user scope and confirmation.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
