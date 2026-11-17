## Description:

Manage and execute periodic heartbeat tasks for trading, memory evaluation, archiving, summaries, and anomaly reporting with state tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuzimaki](https://clawhub.ai/user/wuzimaki)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to coordinate recurring heartbeat checks that trigger crypto trading decisions, memory management, archive maintenance, daily trading summaries, and weekly reviews. It is intended for environments where these automated tasks and state-file updates are expected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes autonomous crypto trading decisions and execution without clear approval controls.

Mitigation: Use only with known accounts, explicit confirmation gates, trading limits, audit logs, and separate operational oversight.

Risk: The skill describes memory-file mutation, cleanup, and archiving without rollback controls.

Mitigation: Restrict write paths, keep backups, and review proposed memory changes before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuzimaki/skills/heartbeat-tasks)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, text]

**Output Format:** [Markdown task guidance with status text and file path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal operation may produce HEARTBEAT_OK; exceptions should include problem details and suggested actions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
