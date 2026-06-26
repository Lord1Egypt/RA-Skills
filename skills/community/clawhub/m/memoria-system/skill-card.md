## Description: <br>
Memoria Memory System helps AI assistants manage local long-term memory with semantic, episodic, procedural, working, and index layers plus backup, migration, rollback, and health-check tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuilinshen](https://clawhub.ai/user/cuilinshen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to initialize and maintain a local memory directory for AI assistants, including daily memory files, backups, rollbacks, and integrity checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can retain sensitive user or project information. <br>
Mitigation: Avoid storing secrets or regulated data, and periodically review memory files and backups. <br>
Risk: Maintenance commands can create, overwrite, delete, or restore files under configured memory and backup paths. <br>
Mitigation: Review config.json, --path, --output, rollback targets, --force, and --fix before running commands. <br>
Risk: Cron automation can run backup or repair actions without an interactive review step. <br>
Mitigation: Enable scheduled jobs only after confirming paths, retention settings, permissions, and backup recovery behavior. <br>


## Reference(s): <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Documentation](artifact/SKILL.md) <br>
- [Configuration Reference](artifact/config.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/cuilinshen/memoria-system) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local maintenance instructions and command examples; bundled scripts may create, modify, back up, or restore files under configured memory paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json/config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
