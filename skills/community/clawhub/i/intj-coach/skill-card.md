## Description:

INTJ Coach guides INTJ users through growth, career, startup, and strategic decision conversations using coaching questions by default and concrete advisory options when users need direct recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run INTJ-oriented coaching or advisory conversations, clarify career and startup direction, turn decisions into next actions, and optionally maintain per-user Markdown records for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store identifiable career, emotional, and personal coaching records tied to platform user IDs.

Mitigation: Require explicit opt-in before creating records, minimize saved content, document retention and deletion paths, and apply restrictive file permissions to the profile directory.

Risk: Proactive reminders and heartbeat follow-up can contact users without enough scoping or consent.

Mitigation: Enable reminders only after user consent, record reminder preferences, and provide a clear way to pause or delete follow-up tracking.

Risk: Saved memory can influence later coaching sessions or expose one user's context to another if IDs are mishandled.

Mitigation: Validate and sanitize user IDs, isolate per-user files, treat stored memory as untrusted context, and confirm identity before loading or updating records.

Risk: The skill discusses emotional distress and life decisions but is not a substitute for professional care.

Mitigation: Keep responses within coaching and advisory boundaries, avoid making decisions for users, and direct users with severe psychological concerns to qualified professional support.

## Reference(s):

- [INTJ Insights](artifact/references/intj-insights.md)
- [INTJ Coach Question Bank](artifact/references/question-bank.md)
- [Advisor Mode Templates](artifact/references/advisor-templates.md)
- [Coach Mode Example](artifact/examples/coach-mode.md)
- [Advisor Mode Example](artifact/examples/advisor-mode.md)
- [ClawHub Skill Page](https://clawhub.ai/lj22503/skills/intj-coach)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands, Python utility usage, and per-user profile, session, and action-record templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are conversational and may include structured action plans, reference cases, follow-up prompts, and local Markdown record updates when profile storage is enabled.]

## Skill Version(s):

2.0.2 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
