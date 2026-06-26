## Description: <br>
AI-powered minimal diary with smart auto-tagging and optional cloud sync. Perfect for daily journaling, work logs, or project tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PrintXDreams](https://clawhub.ai/user/PrintXDreams) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use Mini Diary to maintain a local Markdown journal, add auto-tagged notes, search entries by tag, date, or content, and optionally configure NextCloud sync. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diary entries are stored in local Markdown files and may contain personal or sensitive information. <br>
Mitigation: Install only if local Markdown storage is acceptable for the intended diary content. <br>
Risk: Optional NextCloud sync can expose diary files through cloud sharing, backups, or server-side access. <br>
Mitigation: Leave NEXTCLOUD_SYNC_DIR unset unless cloud sync is intentional, and review NextCloud sharing, backup, and access settings before enabling it. <br>
Risk: Documented sudo chown and docker permission commands can affect file ownership if run against the wrong path. <br>
Mitigation: Verify the exact target path and permission impact before running any administrative command. <br>


## Reference(s): <br>
- [Mini Diary ClawHub page](https://clawhub.ai/PrintXDreams/mini-diary) <br>
- [Mini Diary Usage Guide](docs/usage_guide.md) <br>
- [Mini Diary README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown diary entries with terminal command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes diary content to local Markdown files and can optionally sync to a user-configured NextCloud directory.] <br>

## Skill Version(s): <br>
0.1.2 (source: CHANGELOG, package.json, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
