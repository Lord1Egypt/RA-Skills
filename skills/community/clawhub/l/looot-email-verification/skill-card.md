## Description:

Verify an email address. Use when the user says things like "is jane.doe@example.com a real email", "verify this list of emails before I send" or "check if this address will bounce". Runs through looot, billed per call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walidboulanouar](https://clawhub.ai/user/walidboulanouar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can check one or more email addresses before sending messages. The skill groups results by deliverability and keeps catch-all addresses separate for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email addresses are sent to external verification providers, and each run may incur a charge.

Mitigation: Show the selected endpoint and price and get user approval before running; process only addresses authorized for this check.

Risk: Catch-all results and provider confidence scores may not establish whether a message will reach an inbox.

Mitigation: Keep catch-all addresses separate, review provider status and confidence, and treat results as guidance before deciding to send.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/walidboulanouar/skills/looot-email-verification)
- [looot skill setup](https://looot.ai/skill.md)
- [Email verification skill page](https://looot.ai/agent-skills/email-verification)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-address deliverability status, catch-all status, provider details, confidence and typo suggestions when available; batch counts grouped as deliverable, risky and undeliverable.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
