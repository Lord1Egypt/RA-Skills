## Description:

异步派发编码任务到 OMC (claude -p) 或 OMX (omx exec)，并通过任务文件、后台进程和恢复脚本跟踪执行状态。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiuscut](https://clawhub.ai/user/qiuscut)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this Chinese-language skill to dispatch local coding, analysis, review, and refactoring work to Claude Code or Codex-style CLI agents while tracking task state across restarts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dispatched coding tasks may run with sandbox and approval controls disabled, which can allow broad local file changes or command execution.

Mitigation: Use the skill only for intentional work on trusted repositories, review generated task specs before dispatch, and avoid sandbox-bypass execution unless that behavior is required and understood.

Risk: Persistent recovery and cleanup automation can change task state, delete task directories, or kill tmux sessions.

Mitigation: Review cron and startup-hook commands before enabling them, and run cleanup commands manually first to confirm the target task workspace.

Risk: Task specs, logs, and result files can capture sensitive project context or credentials.

Mitigation: Inspect spec.md and logs for secrets before dispatch or sharing, and avoid embedding API keys or other credentials in task descriptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiuscut/skills/omc-omx-orchestrator)
- [Task schema](references/task-schema.md)
- [Spec template](references/spec-template.md)
- [Recovery guide](references/recovery-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON task metadata descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create local task specs, task metadata, result logs, exit-code files, and recovery commands.]

## Skill Version(s):

4.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
