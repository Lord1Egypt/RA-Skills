## Description:

Mini Diary helps agents keep a minimal Markdown diary with keyword-based auto-tagging, search, statistics, and optional NextCloud sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[printxdreams](https://clawhub.ai/user/printxdreams)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Mini Diary to add daily notes and todos to a local Markdown diary, auto-tag entries, search by tag, date, or content, and optionally sync the diary through NextCloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diary entries may contain sensitive personal or work data and can be copied to a configured NextCloud sync directory.

Mitigation: Leave NEXTCLOUD_SYNC_DIR unset unless sync is intentional, and verify the target sync location and permissions before enabling it.

Risk: DIARY_FILE can direct writes to broad user-scoped paths, which could alter important non-diary files if misconfigured.

Mitigation: Use a dedicated .md diary file and do not point DIARY_FILE at shell profiles, application configuration, or other important files.

Risk: NextCloud administration examples include sudo, docker chown, recursive chown, and cron commands that can affect system files or scheduled jobs if paths are wrong.

Mitigation: Avoid those examples unless the exact target paths are verified and the operator understands the system impact.

## Reference(s):

- [Mini Diary ClawHub Page](https://clawhub.ai/printxdreams/skills/mini-diary)
- [Mini Diary Usage Guide](docs/usage_guide.md)
- [Diary Template](templates/diary_template.md)
- [Sample Diary](examples/sample_diary.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diary entries, command-line search output, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and searches a user-selected Markdown diary file; optional NextCloud sync copies the diary to a configured sync directory.]

## Skill Version(s):

0.1.2 (source: release metadata, CHANGELOG, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
