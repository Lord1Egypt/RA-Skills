## Description:

Delegate PREQSTATION coding tasks to Claude Code, Codex CLI, or Gemini CLI with PTY-safe execution (workdir + background + monitoring).

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonim1](https://clawhub.ai/user/sonim1)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to delegate PREQSTATION-related build, refactor, review, and implementation work to local coding-agent CLIs in mapped workspaces. It is intended for coding task execution that benefits from worktree isolation, background sessions, and progress monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start local coding-agent CLIs that may modify mapped repositories and continue running in the background.

Mitigation: Install and invoke it only when that behavior is intended, and confirm the resolved project path, branch, worktree, engine, and execution mode before use.

Risk: The server security summary flags broad triggering and sandbox-disabled local command execution as behavior that requires review.

Mitigation: Require explicit invocation for sensitive work and avoid sandbox-disabled execution unless the workspace and agent inputs are trusted.

Risk: Incorrect workspace resolution could direct coding work at an unintended repository.

Mitigation: Use exact project mappings, absolute paths, and a per-task git worktree before launching any coding-agent command.

## Reference(s):

- [Preqstation on ClawHub](https://clawhub.ai/sonim1/skills/preqstation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command templates and short text completion summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May launch background local coding-agent sessions and produce progress updates through the host agent environment.]

## Skill Version(s):

0.1.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
