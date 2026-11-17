## Description:

Nex CRM helps agents manage local prospect records, sales pipeline stages, activities, follow-ups, reminders, and CRM exports for freelancers and small businesses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers, one-person agencies, and small businesses use this skill through an agent to add and update prospects, log sales activities, monitor follow-ups, and export CRM data from a local SQLite database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CRM records and exports may contain contact details, notes, messages, reminders, deal values, and other sensitive business information.

Mitigation: Keep ~/.nex-crm private, treat backups and CSV/JSON exports as sensitive records, and review exported files before sharing them.

Risk: The setup script creates local files under ~/.nex-crm and ~/.local/bin and upgrades pip from the configured package index.

Mitigation: Review setup.sh before installation and run it only in a user-controlled environment with a trusted package index.

Risk: Natural-language parsing can place CRM details into the wrong field or activity type.

Mitigation: Review parsed prospect and activity records after creation, and use structured command flags for important updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nexaiguy/skills/nex-crm)
- [Nex AI homepage](https://nex-ai.be)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, files]

**Output Format:** [Plain text CLI output, JSON responses for selected commands, and CSV or JSON export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local CRM data and exports are written under ~/.nex-crm; command output includes a Nex CRM footer for agents to omit in user-facing summaries.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
