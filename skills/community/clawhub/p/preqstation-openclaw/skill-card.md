## Description:

Delegates PREQSTATION coding tasks to Claude Code, Codex CLI, or Gemini CLI with PTY-safe execution, worktree isolation, background execution, and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonim1](https://clawhub.ai/user/sonim1)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to route coding, refactoring, and review tasks into mapped project worktrees using local Claude, Codex, or Gemini CLI engines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run powerful local coding CLIs with approval or sandbox controls disabled, which may modify code, create branches or worktrees, and start background processes.

Mitigation: Install only for trusted repositories, trusted local CLI agents, and trusted task inputs; review generated changes and keep execution scoped to task worktrees.

Risk: Unsafe prompt or path construction in shell commands can cause unintended command behavior.

Mitigation: Prefer safely escaped arguments or prompt files, revise command templates before broad use, and keep sandbox protections enabled by default where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sonim1/skills/preqstation-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell command examples and completion summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a mapped project path, a git worktree, git, and at least one supported local CLI engine.]

## Skill Version(s):

0.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
