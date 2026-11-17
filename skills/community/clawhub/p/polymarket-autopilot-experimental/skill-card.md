## Description:

Experimental skill for automated analysis of public Polymarket markets with paper-trading simulation, LLM cost controls, and Italian-language reports with a mini-summary.

This skill is for research and development only.

## Publisher:

[mauonga](https://clawhub.ai/user/mauonga)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to evaluate public Polymarket markets in a read-only, paper-trading workflow, producing a short Italian report that compares simulated outcomes with LLM costs. It is intended for controlled low-budget experimentation, not wallet-based trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could misread simulated prediction-market analysis as authorization to place real-money trades.

Mitigation: Keep the workflow read-only, do not provide wallet access, and treat outputs as simulated informational reports rather than trading instructions.

Risk: LLM usage costs could exceed the intended low-budget operating envelope.

Mitigation: Enforce the documented execution frequency, weekly budget cap, token tracking, and automatic stop behavior when budget is exceeded.

Risk: The report language is fixed to Italian by default.

Mitigation: Use the skill where Italian output is appropriate, or explicitly modify the reporting language before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mauonga/skills/polymarket-autopilot-experimental)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Italian-language Markdown report with a two-line mini-summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes observed market count, simulated result, detailed LLM costs, simulated net result, and a prudent agent comment.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
