## Description: <br>
Create, manage, and switch between OpenClaw assistant personalities with persisted SOUL and IDENTITY files, backups, heartbeat restoration, and Telegram command access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Robb1010](https://clawhub.ai/user/Robb1010) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to create, preserve, and switch persistent assistant personalities while keeping shared user context separate from personality files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently rewrites OpenClaw identity files and restores the active personality through HEARTBEAT.md. <br>
Mitigation: Install only when persistent personality restoration is intended, and back up SOUL.md, IDENTITY.md, HEARTBEAT.md, openclaw.json, and the personalities directory before installation. <br>
Risk: The skill registers personality management commands for Telegram access. <br>
Mitigation: Review whether Telegram command access is acceptable for the environment, and unregister or remove those commands if remote personality changes are not desired. <br>
Risk: Personality switches modify workspace identity files even though the skill includes backup and rollback safeguards. <br>
Mitigation: Review backups after initial use and keep the default personality intact as the recovery anchor. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Robb1010/personality-switcher) <br>
- [Personality Template Guide](references/personality-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, shell commands, JSON command responses, and generated SOUL.md and IDENTITY.md files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists active personality state, keeps timestamped backups, and preserves USER.md as shared context.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
