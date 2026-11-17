## Description:

Establishes portfolio discipline through a mini IPS, risk budgeting, and no-margin position sizing for Vietnam equity investors; converts recommendations into conditional triggers, invalidation rules, horizon, and confidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teahann](https://clawhub.ai/user/teahann)

### License/Terms of Use:

MIT-0

## Use Case:

External Vietnam equity investors use this skill to create a mini investment policy statement, no-margin sizing policy, per-ticker risk plan, rebalance plan, and review checklist from a confirmed watchlist and optional holdings or risk-profile data.

### Deployment Geography for Use:

Global (focused on Vietnam equity investing)

## Known Risks and Mitigations:

Risk: Portfolio-planning output could be mistaken for broker orders or personalized financial advice.

Mitigation: Treat outputs as planning support, verify assumptions and holdings data, and require user review before acting on target weights.

Risk: Missing holdings, weights, or cash-flow inputs can make position-specific recommendations unreliable.

Mitigation: Disclose assumptions, list required missing data, and provide a general policy when position-specific inputs are unavailable.

Risk: Concentration or leverage risk could increase if guidance is applied outside the skill scope.

Mitigation: Keep leverage at 0%, avoid margin and derivatives, cap single-name exposure, and use conditional triggers and invalidation rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teahann/skills/portfolio-risk-manager)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with five required sections: IPS Mini, Sizing Policy, Per-Ticker Risk Plan, Rebalance Plan, and Next Review Checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, account access, broker execution, margin, derivatives, or leverage; outputs use conditional framing and require user confirmation for target-state changes.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
