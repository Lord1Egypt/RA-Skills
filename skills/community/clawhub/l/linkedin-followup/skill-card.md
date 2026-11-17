## Description:

Manage LinkedIn outreach leads from Google Sheets by finding records, reading live conversation threads, drafting contextual follow-ups, sending approved messages, and updating pipeline status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[10madh](https://clawhub.ai/user/10madh)

### License/Terms of Use:


## Use Case:

Sales and outreach operators use this skill to manage CRM-driven LinkedIn follow-up from a Google Sheet, including reviewing leads, drafting context-aware replies from conversation history, sending approved follow-up messages, and updating pipeline status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an authenticated LinkedIn session and a specified Google Sheet, which can expose account activity and CRM data.

Mitigation: Install only when the user is comfortable granting that access, restrict use to the intended LinkedIn session and Sheet, and require manual confirmation before each send and Sheet write.

Risk: LinkedIn replies and Sheet cells are untrusted content that may influence drafted replies or updates.

Mitigation: Review all drafted messages, inferred statuses, and Sheet changes before execution, and treat scraped thread content and spreadsheet cells as untrusted input.

Risk: Full-thread scraping and persistent logging can retain sensitive conversation history.

Mitigation: Record only the conversation details needed for follow-up, avoid local fallback logging unless intentionally required, and sync or remove local records when they are no longer needed.

Risk: Anti-detection guidance may conflict with platform or organizational compliance expectations.

Mitigation: Remove or replace anti-detection instructions with compliant, user-directed workflows before routine use.

Risk: Unsafe command templates and automated writes can update the wrong CRM row or status.

Mitigation: Confirm the matched lead, row number, message content, and target update range before running gog commands or browser send actions.

## Reference(s):

- [LinkedIn Follow-up on ClawHub](https://clawhub.ai/10madh/skills/linkedin-followup)
- [LinkedIn Follow-up Browser Workflow](references/browser-workflow.md)
- [CRM Sheet Schema](references/sheet-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with draft messages, review tables, and inline shell or browser commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated LinkedIn browser session and gog access to the CRM Google Sheet; sends and Sheet writes should be manually confirmed.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
