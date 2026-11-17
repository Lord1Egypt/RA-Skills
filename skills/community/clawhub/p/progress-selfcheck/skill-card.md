## Description:

Provides periodic progress self-checks with Feishu notifications, Webchat-accessible artifacts, task ledger management, stale-task reactivation, and summary reporting for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ulquoirra](https://clawhub.ai/user/ulquoirra)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and workspace operators use this skill to schedule progress status checks, publish current task and cron summaries, and maintain a lightweight task ledger. It is intended for workflow visibility, with review needed before production or sensitive workspaces because the security evidence flags command reactivation and Feishu sending risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task reactivation can run task-supplied local commands.

Mitigation: Disable automatic reactivation by default or require an explicit allowlist or approval step before any task next command is executed.

Risk: Feishu sending is enabled by default and the security evidence flags unsafe PowerShell command construction.

Mitigation: Disable Feishu sending until the message send path uses safe argument handling and the target account and recipient are reviewed.

Risk: Write access to the task ledger can influence later command execution.

Mitigation: Restrict ledger write access, review ledger updates from untrusted sources, and treat ledger changes as execution-authority changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ulquoirra/skills/progress-selfcheck)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status summaries, JSONL ledger and event records, JSON configuration snippets, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes latest and timestamped progress self-check Markdown under the configured output directory; task ledger and event history are stored as JSONL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
