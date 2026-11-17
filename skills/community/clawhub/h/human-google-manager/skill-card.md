## Description:

Manages Gmail, Calendar, Sheets, Docs, Drive, Contacts, and Tasks with human touch, mandatory confirmation, and automatic to-do detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devnipunajayasekara-ctrl](https://clawhub.ai/user/devnipunajayasekara-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill to manage Google Workspace email, calendars, spreadsheets, documents, files, contacts, and tasks. It is intended for assistant workflows where the agent previews proposed changes and waits for confirmation before account-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require broad Google Workspace access across email, calendars, files, spreadsheets, documents, contacts, and tasks.

Mitigation: Install it only for a Google account where broad Workspace access is acceptable.

Risk: Prepared emails, file moves, calendar changes, spreadsheet edits, or task creation could affect user data if approved without review.

Mitigation: Review each confirmation display carefully before allowing the action to proceed.

Risk: High-impact Workspace changes such as moving files or editing records may be hard to reverse.

Mitigation: Use the skill's confirmation protocol and high-risk warnings to verify the target service, recipients, files, dates, and values before approving.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devnipunajayasekara-ctrl/skills/human-google-manager)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted conversational responses with structured previews and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare Google Workspace actions and request explicit confirmation before execution.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
