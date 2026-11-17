## Description:

Compute the best path when multiple choices compete across vendors, investments, execution options, and strategic decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agisearch](https://clawhub.ai/user/agisearch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and decision-makers use Jupiter to compare multiple viable options, rank routes against objectives and constraints, and identify the best route, fallback route, hidden weaknesses, and next validation step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad option-selection triggers may activate the skill for regulated financial, legal, tax, fiduciary, or procurement approval questions.

Mitigation: Use the output as structured comparison only, and require qualified human review for regulated or approval-bound decisions.

Risk: The skill ranks options from user-provided context and may produce misleading recommendations when objectives, constraints, or missing facts are unclear.

Mitigation: Clarify the objective function, constraints, and unknowns before relying on the ranking, and treat the recommended next step as validation guidance.

## Reference(s):

- [Jupiter ClawHub Skill Page](https://clawhub.ai/agisearch/skills/jupiter)
- [Jupiter README](artifact/README.md)
- [Jupiter Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown routing assessment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes route ranking, tradeoffs, hidden weaknesses, uncertainty notes, and a recommended next step.]

## Skill Version(s):

1.0.0 (source: skill frontmatter, skill.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
