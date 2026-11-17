## Description:

Manages multi-session, multi-stage projects by maintaining and syncing MISSION.md, PROGRESS.md, and NEXT_STEPS.md for seamless long-term progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bono5137](https://clawhub.ai/user/bono5137)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to keep long-running AI projects resumable across sessions by creating and updating structured mission, progress, and next-step documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist cross-session project context in workspace files.

Mitigation: Use it only for projects where persistent progress files are intended, and review PROGRESS.md and MEMORY.md before sharing them with other agents or users.

Risk: Automatic monitoring can observe workspace file changes and update progress without enough user control.

Mitigation: Prefer explicit commands such as checkpoint or mark_milestone, and disable or tightly scope automatic file watching.

Risk: Progress documents may capture sensitive data from logs or configuration files.

Mitigation: Keep logs and secret-bearing JSON/YAML files out of monitored paths.

Risk: Optional third-party tooling or dependencies may expand the runtime environment.

Mitigation: Pin third-party dependencies in an isolated environment before enabling optional watcher or conversion features.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bono5137/skills/ltpm)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown project documents with inline shell commands and optional JSON/YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists project state in workspace files and may use explicit commands or scoped file monitoring to keep progress synchronized.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
