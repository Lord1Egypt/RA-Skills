## Description: <br>
Family medication management skill that helps agents create file-based medication and member records from photos, text, or voice; track inventory, batches, expiry, intake logs, and reminders; and consult bundled references for interactions and pediatric dosing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liucunguang](https://clawhub.ai/user/liucunguang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to manage family medication records, create member profiles, log intake, track expiration dates, and configure medication reminders using local Markdown files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive family health records may be stored in plain local Markdown files and media folders. <br>
Mitigation: Store the data directory in a private encrypted location with restrictive permissions, protect backups, and remove old photos or logs when no longer needed. <br>
Risk: Medication reminders may disclose personal health details through third-party notification services. <br>
Mitigation: Use generic or redacted reminder text and verify every webhook, email, chat, and channel recipient before enabling reminders. <br>
Risk: Medication details, pediatric doses, and interaction checks can be safety-sensitive if copied from photos or reference tables without review. <br>
Mitigation: Confirm extracted medication details, allergies, age, weight, dosage, and interaction guidance with the user and qualified medical sources before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liucunguang/medication-manager) <br>
- [Member Profile Reference](references/member-profile.md) <br>
- [Notification Configuration](references/notifications.md) <br>
- [Storage Layout](references/storage-layout.md) <br>
- [Drug Interactions Reference](references/drug-interactions.md) <br>
- [Pediatric Dosage Reference](references/pediatric-dosage.md) <br>
- [Setup Guide](references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file templates, command examples, and plain-text expiry reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Markdown records and optional reminder configuration; expiry scanning reports are printed as text.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
