## Description:

Structured B2B sales review using original PTC MEDDIC Six-Step methodology, authentic PTC six-step stage gates, and VP-level enhanced gates for deeper review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255)

### License/Terms of Use:

MIT-0

## Use Case:

Sales managers and frontline sales teams use this skill to review opportunities, projects, pipeline forecasts, sales losses, one-on-ones, and customer visits. It helps assess stage status, MEDDIC gaps, win probability, management intervention, and concrete next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer notes may be read from or written to memory without sufficient user consent.

Mitigation: Require explicit confirmation before every customer-memory read or write, and store only sanitized customer names or fixed customer IDs.

Risk: Customer details may be persisted longer than intended.

Mitigation: Avoid storing confidential customer details unless a retention and deletion process is in place.

Risk: Scheduled reminders may be created or changed without clear approval.

Mitigation: Require explicit confirmation before every scheduler or Cron change.

## Reference(s):

- [Skill page](https://clawhub.ai/andyrenxu7255/skills/meddic-b2b-sales-review)
- [clawhub.yaml](artifact/clawhub.yaml)
- [review-opportunity.md](artifact/references/review-opportunity.md)
- [review-project.md](artifact/references/review-project.md)
- [review-pipeline.md](artifact/references/review-pipeline.md)
- [review-loss.md](artifact/references/review-loss.md)
- [review-1on1.md](artifact/references/review-1on1.md)
- [review-visit.md](artifact/references/review-visit.md)
- [six-step.md](artifact/references/methods/six-step.md)
- [meddic.md](artifact/references/methods/meddic.md)
- [stage-gate-validation.md](artifact/references/scoring/stage-gate-validation.md)
- [stage-win-rates.md](artifact/references/scoring/stage-win-rates.md)
- [output-format.md](artifact/references/templates/output-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown sales-review analysis with tables, scorecards, questions, follow-up actions, and reminder guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose customer-memory updates and scheduled reminders when the user confirms they are appropriate.]

## Skill Version(s):

1.4.0 (source: SKILL.md frontmatter, clawhub.yaml, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
