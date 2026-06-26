## Description: <br>
NutriCoach helps users record body metrics and meals, analyze nutrition trends, manage pantry inventory, identify foods from images, and generate diet and recipe recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rainbowlion0320](https://clawhub.ai/user/rainbowlion0320) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Individuals and agent-assisted workflows use this skill to manage personal nutrition records, weight history, pantry inventory, and meal planning. It supports local tracking, reporting, OCR-assisted food entry, exports, backups, and a local dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health and diet records in local plaintext SQLite files. <br>
Mitigation: Use it only on trusted machines, restrict local file access, and encrypt or otherwise protect exported data and backups. <br>
Risk: The local web dashboard is unauthenticated. <br>
Mitigation: Run the dashboard only on a trusted machine and network, and avoid exposing it beyond localhost. <br>
Risk: Cloud OCR can send food or packaging photos to the configured provider. <br>
Mitigation: Prefer local OCR for private images, and use cloud OCR only when the user consents to sharing those images with the provider. <br>


## Reference(s): <br>
- [Architecture](references/ARCHITECTURE.md) <br>
- [Database Schema](references/DATABASE_SCHEMA.md) <br>
- [Feature Guide](references/FEATURE_GUIDE.md) <br>
- [Developer Guide](references/DEVELOPER_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, code snippets, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local database records, reports, JSON or CSV exports, backups, and local dashboard views when the referenced scripts are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
