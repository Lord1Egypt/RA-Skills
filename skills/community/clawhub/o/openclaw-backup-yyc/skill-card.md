## Description:

Backs up and restores selected OpenClaw data under ~/.openclaw using exact Chinese or English trigger commands and confirmation prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teldyang](https://clawhub.ai/user/teldyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to create archives of default OpenClaw configuration, workspace, agent, cron, and media data, then restore those archives when needed. The skill is triggered only by exact Chinese or English backup and restore commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup execution performs external IP lookups to generate an SCP command, which can disclose server network information to third-party services.

Mitigation: Remove the lookup or make it opt-in, and let users provide the host value explicitly before displaying SCP instructions.

Risk: Restore uses tar archive extraction and can accept arbitrary absolute backup paths.

Mitigation: Validate archive members before extraction, reject unsafe paths, and restrict restore inputs to expected backup locations unless the user explicitly approves another path.

Risk: Restore operations rename existing OpenClaw folders and copy archived directories into place.

Mitigation: Require confirmation for every restore path and recommend taking a fresh backup before restoring.

Risk: Operational prompts include unrelated promotional links.

Mitigation: Remove promotional links from backup and restore prompts so users can focus on operational warnings and file-handling decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teldyang/skills/openclaw-backup-yyc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown and terminal text with shell commands and backup archive files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates OpenClaw-Backup-YYC timestamped tar.gz archives and can restore workspace, agents, cron, media, and extracted configuration files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
