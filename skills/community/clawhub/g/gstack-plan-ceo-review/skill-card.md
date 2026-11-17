## Description:

Plan Ceo Review guides agents through CEO/founder-style plan reviews across scope expansion, selective expansion, hold-scope, and scope-reduction modes, challenging assumptions and surfacing implementation, testing, security, observability, rollout, and design risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loocor](https://clawhub.ai/user/loocor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical leads, and product builders use this skill to review plans for ambition, scope fit, failure modes, test coverage, security, observability, rollout readiness, and long-term product direction. It is intended for planning and review workflows where the agent should ask structured decision questions before changing scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect repository history, diffs, stashes, TODO markers, and project documents as part of its planning review.

Mitigation: Use it only in repositories where that level of local project inspection is acceptable, and review its findings before acting on recommendations.

Risk: Expansion modes may create local planning notes or TODO updates that affect project documentation.

Mitigation: Review generated planning or TODO changes before accepting, committing, or promoting them.

Risk: The skill is intentionally opinionated and may challenge scope or propose broader work than the user initially requested.

Mitigation: Treat scope changes as opt-in decisions and keep the user's selected mode as the controlling boundary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loocor/skills/gstack-plan-ceo-review)
- [Loocor publisher profile](https://clawhub.ai/user/loocor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style review narrative with structured questions, tables, ASCII diagrams, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask sequential decision questions and, in expansion-oriented modes, may propose or create local planning and TODO Markdown for user review.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
