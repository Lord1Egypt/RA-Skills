## Description:

Novel Forge guides agents through stateful long-form fiction projects, including setup, role-to-model mapping, canon planning, chapter drafting, review, recovery, and memory tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[228998098](https://clawhub.ai/user/228998098)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent operators use this skill to start, continue, recover, and maintain serialized fiction projects with file-backed state. It supports single-agent work and staged multi-agent collaboration for worldbuilding, characters, outlines, style, drafting, review, and memory updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks to read local OpenClaw model configuration and may expose model inventory or configuration details.

Mitigation: Review before installing, use a sanitized model-inventory source where possible, and avoid exposing unrelated local configuration.

Risk: Included scripts create or update project files and accept output paths that can target arbitrary writable locations.

Mitigation: Run only in a constrained workspace, avoid elevated privileges, keep backups of novel project files, and do not pass arbitrary output paths.

Risk: The server security verdict flags the release as suspicious because of broad local configuration access and file-writing behavior.

Mitigation: Follow the server guidance: review the skill before installing and limit execution to trusted workspaces and intended project directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/228998098/skills/novel-forge)
- [Workflow](artifact/references/workflow.md)
- [External State Machine](artifact/references/state-machine.md)
- [Novel Forge Runbook](artifact/references/runbook.md)
- [Schemas](artifact/references/schemas.md)
- [Main Session Constraints](artifact/references/main-session-constraints.md)
- [Continuation Checklist](artifact/references/continuation-checklist.md)
- [Agent Prompt Templates](artifact/references/prompts.md)
- [Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, structured JSON project state, file scaffolds, and shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are staged around project state files, chapter markdown, role-to-model mappings, and recovery checkpoints.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
