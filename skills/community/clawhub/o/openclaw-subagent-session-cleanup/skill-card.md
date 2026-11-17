## Description:

Clean up accumulated subagent and cron:run child sessions in OpenClaw to fix slow subagent startup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrddrl](https://clawhub.ai/user/lrddrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill when accumulated child session records make subagents slow to start. It guides cleanup of subagent and cron run session records while preserving main and channel sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells agents to run an unbundled local cleanup script that can modify persistent OpenClaw session data.

Mitigation: Inspect the actual cleanup.ps1 script in the target environment, run a dry-run first, and back up sessions.json before cleanup.

Risk: Using the CleanJsonl option can delete .jsonl conversation history files.

Mitigation: Avoid CleanJsonl unless conversation history deletion is intentional, and back up .jsonl history files before using it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrddrl/skills/openclaw-subagent-session-cleanup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run, backup, and history-deletion cautions for cleanup operations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
