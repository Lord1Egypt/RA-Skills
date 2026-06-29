## Description: <br>
Backs up and restores OpenClaw data by guiding users through archive creation, restore steps, backup scheduling, and backup rotation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phenixstar](https://clawhub.ai/user/phenixstar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to create local backups of OpenClaw configuration, credentials, agent state, workspace files, sessions, and scheduled tasks, then restore or rotate those backups when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives can contain API keys, tokens, session data, private workspace files, and scheduled tasks. <br>
Mitigation: Store backup archives encrypted or in a restricted location, and treat them as highly sensitive. <br>
Risk: Restore commands can interrupt OpenClaw and replace current local state. <br>
Mitigation: Verify the archive before restoring, stop OpenClaw during restore, and keep a rollback copy of the existing state. <br>


## Reference(s): <br>
- [Restore OpenClaw from Backup](artifact/references/restore.md) <br>
- [Project homepage](https://github.com/PhenixStar/openclaw-skills-collection) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local backup archives and restore steps that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
