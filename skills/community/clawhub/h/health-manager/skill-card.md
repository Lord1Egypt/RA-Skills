## Description:

Health Manager helps agents record, organize, analyze, import, export, and report on blood pressure, heart rate, exercise, medication, and reminder data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to maintain a local personal health log, review trends, manage medication and health reminders, and generate daily, weekly, or handbook-style reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health information is stored locally in an unencrypted SQLite database.

Mitigation: Install only when local storage is acceptable, restrict filesystem access to the database, and treat the database as private medical data.

Risk: Imports can process untrusted CSV or JSON health data.

Mitigation: Import only trusted files and review source data before adding it to the health database.

Risk: Exports and generated reports may contain private medical records.

Mitigation: Share exported files and reports only with intended recipients, and store or delete them according to the user's privacy requirements.

Risk: CSV exports can expose users to spreadsheet formula execution risks.

Mitigation: Sanitize exported CSV values before opening them in spreadsheet software.

Risk: Documented cloud, wearable, OAuth, or simulated-login integrations would expand privacy and security exposure.

Mitigation: Do not implement or enable those integrations without a separate privacy and security review.

## Reference(s):

- [Health Manager ClawHub Listing](https://clawhub.ai/harrylabsj/skills/health-manager)
- [README](README.md)
- [User Guide](USER_GUIDE.md)
- [Health Manager Design](design/health-manager-design.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [CLI text, Markdown reports, CSV or JSON exports, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores data locally and can generate daily, weekly, and handbook-style health reports.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
