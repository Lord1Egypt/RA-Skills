## Description: <br>
Task Queue by Model Source routes tasks into per-model-source FIFO queues with support for dependencies, context passing, retries, and failure handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bg1avd](https://clawhub.ai/user/bg1avd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to route delegated work into per-model-source queues, track dependencies, dispatch pending tasks, and report completion or failure status. It is intended for local task orchestration where users want persistent queue files and optional heartbeat or cron-backed dispatch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent background execution and broad triggers could run queued work without clear user control. <br>
Mitigation: Install only if persistent local task queues are desired, review pending and running queue files regularly, and keep automatic dispatcher triggers disabled unless explicitly needed. <br>
Risk: First-run setup may create local queue files and register heartbeat or cron-backed dispatcher entries. <br>
Mitigation: Confirm the exact queue directory, heartbeat entry, and cron payload before setup, and verify there is a clear stop, uninstall, or rollback path. <br>
Risk: Queued tasks can spawn subagents and pass context from dependency results into later tasks. <br>
Mitigation: Avoid placing sensitive data in queued task descriptions or dependency summaries unless the selected model source and subagent runtime are approved for that data. <br>


## Reference(s): <br>
- [Queue Schema Reference](artifact/queue-schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/bg1avd/model-queue) <br>
- [Publisher Profile](https://clawhub.ai/user/bg1avd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown and chat text with JSON queue files and shell/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates one FIFO JSON queue per model source, emits task status notifications, and may register heartbeat or cron-backed dispatcher entries on first use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and target metadata; artifact metadata reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
