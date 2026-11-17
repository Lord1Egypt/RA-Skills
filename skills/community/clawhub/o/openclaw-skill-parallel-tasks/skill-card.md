## Description:

Execute multiple tasks in parallel with timeout protection, error isolation, and real-time progress feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiukui666](https://clawhub.ai/user/qiukui666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run independent research, analysis, implementation, polling, or batch tasks concurrently while receiving timeout, error, and progress feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parallel task dispatch can amplify unintended file-write, account-changing, or public-posting actions.

Mitigation: Use explicit task lists, keep concurrency low, and review the effects of spawned sessions before high-impact tasks.

Risk: Broad activation can send ambiguous or dependent work into multiple sessions.

Mitigation: Use this skill only for clearly independent tasks; keep dependent or shared-state work sequential.

Risk: Long-running or excessive parallel work can consume local and agent-session resources.

Mitigation: Set reasonable per-task timeouts and use the max-concurrency option to limit active sessions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/qiukui666/skills/openclaw-skill-parallel-tasks)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal progress output and Markdown-style summary tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aggregates task status, duration, and error details; exits nonzero when any task fails or times out.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
