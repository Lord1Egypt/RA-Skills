## Description:

Privacy Eraser helps agents find exposed personal information online, recommend removal paths, generate privacy complaint templates, and set up monitoring when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tykoo-eth](https://clawhub.ai/user/tykoo-eth)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and support agents use this skill to identify exposed personal information, choose platform-specific removal or escalation paths, and draft privacy, legal, GDPR, DMCA, or regulator complaint text for review before submission.

### Deployment Geography for Use:

Global, with specific guidance for China, EU/GDPR, and US privacy or copyright complaint contexts.

## Known Risks and Mitigations:

Risk: The skill may use logged-in browser sessions to submit reports, send messages, or take other external actions without enough user control.

Mitigation: Keep the skill in draft-and-guidance mode unless the user explicitly approves each destination, action, and final text before submission.

Risk: The skill may read user identity data, request or upload identity documents, store screenshots, or create case records involving sensitive personal information.

Mitigation: Use the minimum necessary personal data, redact identity materials whenever possible, and confirm destination, retention, and deletion expectations before handling evidence.

Risk: Recurring monitoring can continue collecting personal information after the immediate removal task is complete.

Mitigation: Create monitoring only after the user approves the exact schedule, search terms, notification behavior, retention period, and cancellation path.

Risk: Complaint or takedown templates can create legal or platform-policy risk if used with inaccurate claims, especially DMCA notices.

Mitigation: Require the user to verify facts and use DMCA language only for genuine copyright claims before sending any notice.

## Reference(s):

- [Privacy Eraser ClawHub listing](https://clawhub.ai/tykoo-eth/skills/privacy-eraser)
- [Platform reporting entry guide](artifact/platforms.md)
- [Privacy legal basis reference](artifact/legal_basis.md)
- [Generic privacy complaint template](artifact/generic_privacy.md)
- [GDPR data erasure request template](artifact/gdpr_request.md)
- [DMCA takedown notice template](artifact/dmca_takedown.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with complaint templates, checklists, platform-specific steps, and occasional command or schedule snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose external reports, legal notices, browser actions, monitoring schedules, and evidence records; submissions and sensitive data handling require explicit user review.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
