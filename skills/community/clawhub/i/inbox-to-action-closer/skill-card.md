## Description:

This orchestration skill processes caller-supplied raw work-item data from Slack, GitHub, calendar, Notion, Trello, and email into a merged, prioritized action board with owners, due dates, reply drafts, and follow-up questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[honouralexwill](https://clawhub.ai/user/honouralexwill)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, teams, and developers use this skill to turn raw pending-work data from communication, code, calendar, and task systems into a single draft action board for review and follow-up planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository guidance files include unrelated agent-control instructions.

Mitigation: Review repository guidance before installation and do not let it override the agent's normal policies.

Risk: Rendered Markdown may include source-supplied content with weaker sanitization.

Mitigation: Prefer the structured JSON output for automation, or sanitize and review rendered Markdown before sharing it.

Risk: Heuristic scoring and deduplication can miss context or rank items unexpectedly.

Mitigation: Treat the board as a draft, verify source URLs, and confirm priorities before acting.

Risk: Development dependencies may need updates before local test or development-server use.

Mitigation: Update and review development dependencies before running tests or dev servers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/honouralexwill/skills/inbox-to-action-closer)
- [Publisher profile](https://clawhub.ai/user/honouralexwill)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown action board and structured JSON action-board object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only output with source URLs, priority tiers, skipped-source details, and item counts.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
