## Description:

Build and run a behavior-first personal planning, triage, and decision agent that learns a user's values, goals, recurring problems, friction patterns, and decision standards over time, then gives strong recommendations for immediate action, multi-problem triage, dilemmas, 3-6 month planning, weekly review, and proactive heartbeat follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lakendocean](https://clawhub.ai/user/lakendocean)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent for long-term personal planning, decision support, prioritization, weekly review, and proactive follow-up. It is intended for behavior-first guidance that turns values, goals, and recurring patterns into near-term actions while preserving the user's agency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may store sensitive personal details in long-lived plaintext workspace files.

Mitigation: Decide what categories of personal information may be stored before use, review proposed durable file updates, and periodically delete or trim stored profile files.

Risk: The agent may treat temporary moods or one-time statements as durable user facts.

Mitigation: Keep identity and direction changes tentative until they are repeated or confirmed across later interactions.

Risk: Personal planning recommendations can be over-relied on for serious life decisions.

Mitigation: Use recommendations as decision support, preserve user agency, and seek qualified professional help where legal, medical, financial, mental health, or safety stakes are involved.

## Reference(s):

- [File Contracts](references/file-contracts.md)
- [Judgment System](references/judgment-system.md)
- [Bootstrap Questionnaire](references/bootstrap-questionnaire.md)
- [Interaction Modes](references/interaction-modes.md)
- [Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown responses and Markdown workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose updates to durable workspace files such as USER.md, IDENTITY.md, GOALS.md, DECISION_RULES.md, DECISIONS.md, and HEARTBEAT.md.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
