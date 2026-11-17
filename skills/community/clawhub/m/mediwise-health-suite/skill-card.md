## Description:

Family health management suite for health records, diet tracking, weight management, and wearable sync, with local SQLite storage by default and optional cloud features requiring explicit setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juneyaooo](https://clawhub.ai/user/juneyaooo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and families use this OpenClaw skill to record health records, diet, weight, wearable data, and doctor-visit preparation summaries. Developers can deploy it locally with SQLite and optional integrations for model, food, wearable, or backend services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health data is stored and exported by the skill.

Mitigation: Protect SQLite data, configuration, and backup files as sensitive medical records and do not share generated backups with unauthorized users.

Risk: Shared or multi-user deployments can expose records if owner identity is not enforced.

Mitigation: Use the skill as a single-user local tool unless owner_id is enforced by trusted platform identity for each user.

Risk: Credentials and API keys may be exposed if provided through chat or logs.

Mitigation: Enter passwords and API keys only through local terminal configuration flows; do not place secrets in conversation text.

Risk: Optional external model, wearable, food, or backend services can transmit sensitive content outside the local environment.

Mitigation: Enable external services only when needed, prefer trusted local or self-hosted endpoints, and avoid custom remote HTTP model endpoints for sensitive records.

Risk: Backup restore can import untrusted data into the local health store.

Mitigation: Restore backups only from trusted sources and keep backup archives protected.

## Reference(s):

- [MediWise Health Suite Homepage](https://github.com/JuneYaooo/mediwise-health-suite)
- [MediWise Health Management Overview](docs/HEALTH-MANAGEMENT-OVERVIEW.md)
- [Installation Guide](docs/INSTALLATION.md)
- [Agent Setup Guide](docs/AGENT_SETUP.md)
- [Cycle, Attachments, and Multi-Tenancy](mediwise-health-tracker/references/cycle-attachments-multitenancy.md)
- [Drug Safety and Briefing](mediwise-health-tracker/references/drug-briefing.md)
- [Intake, Query, and Vision](mediwise-health-tracker/references/intake-query-vision.md)
- [Visit Preparation Summary](mediwise-health-tracker/references/visit-prep.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown and plain text responses with command examples, configuration guidance, and optional generated report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local SQLite storage by default; optional external services are activated only through user configuration.]

## Skill Version(s):

2.0.8 (source: server release evidence; artifact frontmatter and package.json report 2.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
