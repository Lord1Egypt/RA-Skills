## Description:

Connect local agents to OnePilot for event recommendations, optional mailbox-code and calendar availability help, consent-based memory and feedback, application form support, and organizer-only event management or registration export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[y09749204-gif](https://clawhub.ai/user/y09749204-gif)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use OnePilot CLI to let local agents bind to a OnePilot account, recommend OPC and AI startup events, manage consent-based memory and feedback, prepare application answers, and assist organizer accounts with workbench tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill binds a OnePilot account and stores a local agent token.

Mitigation: Install only when account binding is acceptable, keep the local token file private, and never paste, commit, upload, or share it.

Risk: Selected preferences, availability, application profile details, answer examples, and event feedback may be sent to OnePilot cloud.

Mitigation: Send or save this data only after normal user-agent interaction and clear user consent.

Risk: QR downloading and custom output paths are broader than the core event-assistant workflow.

Mitigation: Avoid custom QR URLs and custom --output paths unless the source and destination are clearly trusted.

Risk: Organizer CSV exports can contain data that is unsafe to open directly in spreadsheet tools.

Mitigation: Treat exported CSV files as untrusted, review them before opening, and avoid forwarding raw exports unnecessarily.

Risk: Recommendation or email wording may affect user decisions or external communications.

Mitigation: Review recommendation summaries, application drafts, and email text before sending or acting on them.

## Reference(s):

- [OnePilot Website](https://onepilot.zeabur.app)
- [ClawHub Skill Page](https://clawhub.ai/y09749204-gif/skills/onepilot-skill)
- [Publisher Profile](https://clawhub.ai/user/y09749204-gif)
- [README](README.md)
- [Security Policy](SECURITY.md)
- [Platform Adapter Notes](references/adapters.md)
- [Activity Intent Few-shots](references/activity-intent-few-shots.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and structured JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing output may include local CLI commands, OnePilot event URLs, application-answer drafts, organizer CSV export guidance, and reminders to obtain user consent before saving or sending data.]

## Skill Version(s):

0.1.24 (source: server release, VERSION, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
