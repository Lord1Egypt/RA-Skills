## Description:

Git工作流 is a Chinese-language Git workflow assistant for branch management, conflict resolution, conventional commit guidance, rollback, recovery, cleanup, and repository workflow questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to receive Chinese-language Git workflow guidance and suggested commands for branch management, merge conflict handling, commit message conventions, rollback, recovery, cleanup, and collaboration practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes broad Git workflow guidance and examples of destructive commands that can permanently change or delete repository work.

Mitigation: Use it only for explicit Git tasks; review the exact repository state, back up needed work, and intentionally approve destructive commands before running them.

Risk: Suggested cleanup, history rewrite, reset, reflog expiry, or aggressive garbage collection commands can be unsafe when applied without context.

Mitigation: Preview and narrow commands where possible, confirm the target repository and paths, and avoid hard reset, force clean, history rewrite, BFG deletion, reflog expiry, or aggressive garbage collection unless deliberately required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/git-workflow-cn-paid)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and occasional JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Git commands that require repository-state review before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
