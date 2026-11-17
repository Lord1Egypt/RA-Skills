## Description:

Gift Occasion Planner helps agents maintain gift profiles, track upcoming occasions, recommend non-repeating budget-aware gifts, create action plans, log gift history, and export calendar reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users and personal productivity agents use this skill to remember birthdays, anniversaries, holidays, and other gift occasions, then turn recipient profiles and gift history into timely recommendations and action plans. It is most useful for individuals or families managing recurring occasions, personal budgets, and calendar reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated gifts.json and ICS files can contain personal notes, budgets, interests, taboo gift information, and recipient details.

Mitigation: Review generated JSON and ICS files before sharing them or importing them into a cloud-synced calendar.

Risk: One-time occasions may be represented through month-day recurrence behavior and can be treated like annual events.

Mitigation: Review one-time occasions during planning and remove or update them after the event if they should not recur.

## Reference(s):

- [Gift Intelligence Reference](references/gift-intelligence.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, plus local JSON data and ICS calendar files when the script is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local gifts.json storage and can export all-day ICS reminder events.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter; server release metadata agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
