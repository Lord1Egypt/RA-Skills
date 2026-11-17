## Description:

AI-powered multilingual virtual salesperson for 24/7 global customer reception, client retention, real-time boss alerts, and continuous sales optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanlv123](https://clawhub.ai/user/zhanlv123)

### License/Terms of Use:

MIT-0

## Use Case:

Foreign trade sellers, company operators, and sales teams use this skill to create or update an Ieasysell digital-human reception link, support multilingual customer intake, and notify the business owner about new visitor activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a live Ieasysell login token.

Mitigation: Use a scoped and revocable credential where possible, rotate it regularly, and remove the skill if token access is no longer needed.

Risk: The skill can create, update, or reset digital-human reception settings.

Mitigation: Limit who can run the skill, test configuration changes before production use, and review generated or changed reception links in Ieasysell.

Risk: The skill pulls visitor records and can store or notify customer contact details.

Mitigation: Define customer privacy and retention controls, minimize contact details in notifications, and restrict notification recipients.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhanlv123/skills/ieasysell)
- [Ieasysell Application](https://app.ieasysell.com)

## Skill Output:

**Output Type(s):** [Text, Notifications, Configuration, Guidance]

**Output Format:** [Plain text status messages, customer-activity notifications, reception URLs, and a JSON-like execution result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Ieasysell credentials and company, product, market, and sync interval configuration.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
