## Description:

Judgment Loop helps agents turn consequential choices, uncertain claims, recurring failures, serious learning, and evidence-based reviews into provisional judgments, discriminating tests, and user-owned action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirsws](https://clawhub.ai/user/sirsws)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill when a meaningful decision, evidence claim, learning goal, or review outcome has unresolved uncertainty. It helps the agent keep the user responsible for the choice while separating facts, assumptions, failure conditions, tests, and next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npx installation examples can fetch a changing skills CLI at install time.

Mitigation: Prefer the ClawHub install path, or verify and pin the skills CLI before using npx examples.

Risk: The evaluation assets define a review protocol but do not establish a validated behavioral baseline for the skill.

Mitigation: Treat the evaluation cases as review scaffolding until a raw-output-preserving, independently reviewed run is completed.

Risk: Decision-support output can be over-applied to simple, low-risk, or already specified tasks.

Mitigation: Follow the skill's conservative routing rule and keep low-cost reversible tasks outside the full judgment loop.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sirsws/skills/judgment-loop)
- [Decision mode reference](references/decision.md)
- [Research mode reference](references/research.md)
- [Learning mode reference](references/learning.md)
- [Review mode reference](references/review.md)
- [Evaluation protocol](evals/trigger-cases.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text responses with optional headings and citations when reviewing evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs emphasize a provisional judgment, evidence, failure condition, discriminating test, user-owned action, and review trigger.]

## Skill Version(s):

1.1.2 (source: server release metadata and README badge)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
