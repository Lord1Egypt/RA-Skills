## Description:

Relationship Buddy helps users maintain a private personal CRM with contact details, important dates, interaction history, reminders, gift ideas, conversation starters, and relationship health summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT

## Use Case:

Individuals use this skill to remember details about important people in their lives, track interactions and key dates, and receive timely prompts for check-ins, gifts, and conversation starters. It is a personal CRM and explicitly not a therapy, counseling, or mental health tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can overwrite existing Relationship Buddy data files if rerun.

Mitigation: Back up the data directory before setup and avoid rerunning the setup prompt over an existing installation.

Risk: The skill stores sensitive relationship data such as names, birthdays, family details, notes, and interaction history locally.

Mitigation: Keep the workspace on a protected device, use device-level encryption where appropriate, and review file permissions for local data files.

Risk: Automatic contact updates may save casual mentions that the user did not intend to preserve.

Mitigation: Review proposed updates and ask before saving sensitive or ambiguous relationship details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-relationship-buddy)
- [README](README.md)
- [Security audit](SECURITY.md)
- [Setup prompt](SETUP-PROMPT.md)
- [Dashboard companion spec](dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with local JSON data files, configuration JSON, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and updates local relationship records; optional CSV migration appends contacts to a local JSON file.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
