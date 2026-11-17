## Description:

Clean up accumulated subagent and cron:run child sessions in OpenClaw to improve slow subagent startup caused by large sessions.json files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrddrl](https://clawhub.ai/user/lrddrl)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to stop the gateway, run a cleanup workflow for accumulated child-session records, and restart the gateway when subagent startup slows down.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow runs a relative PowerShell cleanup script that is not bundled in the artifact.

Mitigation: Inspect the script from a trusted path before execution and use the dry-run option before making changes.

Risk: Cleanup options can modify sessions.json and may delete .jsonl conversation-history files.

Mitigation: Back up sessions.json and conversation history before cleanup, and avoid delete options unless history loss is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrddrl/skills/openclaw-session-cleanup-ruodon)
- [Publisher profile](https://clawhub.ai/user/lrddrl)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a dry-run mode and options that preserve or delete .jsonl conversation-history files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
