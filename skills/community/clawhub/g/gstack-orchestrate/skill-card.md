## Description: <br>
Gstack Orchestrate takes a gstack implementation plan, decomposes it into parallel wave-based tasks, dispatches isolated-worktree Claude Code subagents, verifies each wave, and hands off to review and ship workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to execute an approved gstack implementation plan through coordinated parallel subagents, wave verification, local commits, and review/ship handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill coordinates high-impact repository changes through subagents, local commits, and review/ship handoff. <br>
Mitigation: Use it on a clean non-base branch, review the task breakdown before approving dispatch, and inspect resulting commits before confirming ship handoff. <br>
Risk: Telemetry can include repository or branch metadata when enabled. <br>
Mitigation: Keep telemetry off when repository or branch metadata is sensitive; the evidence states remote telemetry is opt-in and local telemetry is disclosed. <br>
Risk: Isolated worktree branches can accumulate after orchestration runs. <br>
Mitigation: Review and clean leftover branches manually instead of relying on automatic deletion. <br>


## Reference(s): <br>
- [Gstack Orchestrate repository](https://github.com/kaicianflone/gstack-orchestrate) <br>
- [Gstack Orchestrate on ClawHub](https://clawhub.ai/kaicianflone/gstack-orchestrate) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline bash blocks, task plans, JSONL state records, commit summaries, and final reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user approval before dispatch; persists local orchestration state and may write local or opt-in remote telemetry.] <br>

## Skill Version(s): <br>
1.6.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
