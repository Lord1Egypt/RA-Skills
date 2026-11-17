## Description:

Run Codex CLI, Claude Code, OpenCode, or Pi Coding Agent via background process for programmatic control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[branexp](https://clawhub.ai/user/branexp)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to launch and supervise coding agents in focused work directories for non-interactive implementation, review, and maintenance tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe autonomous execution modes can run coding agents with broad authority.

Mitigation: Prefer sandboxed or approval-gated modes, use narrow temporary worktrees, and review diffs before commit, push, PR creation, or PR comments.

Risk: Prompt history, session logs, or generated review comments can disclose sensitive information if published unintentionally.

Mitigation: Publish prompt history and session logs only after intentional review.

Risk: Unpinned global installs can introduce supply-chain drift.

Mitigation: Avoid unpinned global npm installs where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/branexp/skills/giga-coding-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires one of claude, codex, opencode, or pi to execute the suggested agent commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
