## Description:

Calculates risk-based position sizes for long stock trades using fixed fractional, ATR-based, and Kelly Criterion methods with portfolio constraint checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to calculate share counts and risk budgets for long stock trades from account size, entry price, stop-loss distance, ATR, Kelly inputs, and optional portfolio concentration limits. It supports risk-management analysis and does not provide buy or sell signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat position-sizing output as investment advice or as a recommendation to buy or sell a security.

Mitigation: Present the output as risk-management math only, and require users to confirm their own trading assumptions before acting.

Risk: Incorrect account size, entry, stop-loss, ATR, Kelly, or concentration inputs can produce unsuitable share counts or risk budgets.

Mitigation: Validate all inputs with the user and prefer conservative rounding before using results for a real trade.

Risk: The local script saves JSON and Markdown reports that may contain sensitive portfolio or trading assumptions.

Mitigation: Run it in a trusted workspace, choose the output directory deliberately, and review or remove saved reports when they contain sensitive data.

## Reference(s):

- [Sizing Methodologies](references/sizing_methodologies.md)
- [ClawHub Skill Page](https://clawhub.ai/clawdiri-ai/skills/medici-investments-position-sizer-dv)
- [Publisher Profile](https://clawhub.ai/user/clawdiri-ai)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [CLI guidance with stdout summaries and timestamped JSON and Markdown position-sizing reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved under the configured output directory; calculations depend on user-supplied financial inputs.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
