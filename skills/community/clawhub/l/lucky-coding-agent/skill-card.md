## Description:

Delegates coding tasks to Codex, Claude Code, OpenCode, or Pi agents through PTY-enabled bash sessions, including background workflows for building, refactoring, and pull request review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rmbell09-lang](https://clawhub.ai/user/rmbell09-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate substantial coding, refactoring, and pull request review work to command-line coding agents while tracking long-running background sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: No-approval coding-agent execution can run broad commands and modify workspace or repository state.

Mitigation: Prefer sandboxed or approval-gated modes, avoid documented no-approval workflows, and require human review before dependency installs, commits, pushes, pull request creation, or host notification commands.

Risk: Untrusted issue or pull request text can be copied into shell command templates.

Mitigation: Treat external text as data, quote or isolate it before use, and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rmbell09-lang/skills/lucky-coding-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose background agent sessions and follow-up monitoring commands.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
