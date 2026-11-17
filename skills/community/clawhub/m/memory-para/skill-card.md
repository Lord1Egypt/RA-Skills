## Description:

Manage and maintain memory systems using the Root + PARA hybrid architecture for memory maintenance, daily log distillation, and core workspace file updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hugo-zhu](https://clawhub.ai/user/hugo-zhu)

### License/Terms of Use:


## Use Case:

OpenClaw users and agents use this skill to distill noisy daily conversation logs into a Root + PARA memory workspace. It routes durable preferences, rules, tool assumptions, identity details, project progress, domain knowledge, static resources, archives, and global memory index updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify long-term memory files that influence future agent behavior, identity, tool assumptions, and user profile data.

Mitigation: Run memory maintenance manually or require reviewed diffs before accepting changes, and keep versioned backups of memory files.

Risk: The maintenance SOP deletes processed daily logs after archiving, which can remove raw evidence if distillation or archival is incorrect.

Mitigation: Retain raw logs until the archive append and distilled memory updates have been reviewed and confirmed.

## Reference(s):

- [Skill source](artifact/SKILL.md)
- [README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/hugo-zhu/skills/memory-para)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown file updates and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update long-term memory files and archive or remove processed raw logs during maintenance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
