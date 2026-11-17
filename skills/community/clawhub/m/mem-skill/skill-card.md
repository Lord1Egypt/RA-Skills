## Description:

Mem Skill gives agents a workspace-local memory layer that retrieves prior knowledge and records reusable solutions with user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oliguo](https://clawhub.ai/user/oliguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give coding assistants a local, persistent memory for reusable workflows, preferences, and skill-specific experience across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to run as an always-on workspace memory layer and persist conversation-derived data.

Mitigation: Install only where persistent local memory is intentional, and periodically audit or clear knowledge-base, experience, and log.md.

Risk: Shared or sensitive workspaces may expose retained memory entries to later agent sessions or collaborators.

Mitigation: Keep the skill out of shared or sensitive workspaces unless retention and redaction practices are reviewed.

Risk: QMD/global setup and URL ingestion are called out by security guidance as areas needing additional hardening.

Mitigation: Avoid QMD/global setup and URL ingestion until dependencies are pinned, the init.sh path-injection issue is fixed, and retention controls are added.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oliguo/skills/mem-skill)
- [Memory Engine Architecture](references/engines.md)
- [QMD Memory Engine Reference](references/qmd-engine.md)
- [QMD](https://github.com/tobi/qmd)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration/file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local knowledge-base, experience, log, and optional .mem-skill.config.json files after user approval.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
