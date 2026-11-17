## Description:

Personal health data management and intelligent diet recommendation system for tracking body metrics, meals, nutrition trends, pantry inventory, OCR food recognition, and recipe recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rainbowlion0320](https://clawhub.ai/user/rainbowlion0320)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage personal nutrition and health data locally: set profiles, log body metrics and meals, analyze nutrition trends, manage pantry inventory, scan food labels, and generate recipe or diet recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health and nutrition data may be exposed or modified if the dashboard is run on an untrusted network.

Mitigation: Bind the dashboard to 127.0.0.1, add authentication before network exposure, and keep exported or backed-up database files secured.

Risk: Cloud OCR can send private food packaging images or nutrition data to a third-party provider.

Mitigation: Use local OCR for private images when available, or configure cloud OCR only with a provider the user trusts.

Risk: Per-user local data depends on user-selected names and generated files.

Mitigation: Use simple usernames and avoid sharing generated database, export, or backup files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rainbowlion0320/skills/nutricoach)
- [Architecture](references/ARCHITECTURE.md)
- [Database Schema](references/DATABASE_SCHEMA.md)
- [Feature Guide](references/FEATURE_GUIDE.md)
- [Developer Guide](references/DEVELOPER_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Executing the guided commands can create local SQLite databases, JSON/CSV exports, backups, and a local dashboard.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
