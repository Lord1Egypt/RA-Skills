## Description:

Analyze perpetual futures positions directly in Claude Code - liquidation price, risk/reward, PnL, and probability-based trade plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[farisalahmad714](https://clawhub.ai/user/farisalahmad714)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and traders use this skill to submit perpetual futures position parameters to the Perpulator API and receive liquidation, risk/reward, PnL, and trade-plan analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill unnecessarily prints the user's API key.

Mitigation: Check only whether PERPULATOR_API_KEY is present and avoid running the skill where command output or environment values may be logged.

Risk: The security evidence reports an unsafe shell-command pattern for user-supplied trade inputs.

Mitigation: Validate symbol, side, price, margin, leverage, stop-loss, take-profit, and current-price values before use, and build request JSON with safe serialization.

## Reference(s):

- [Perpulator homepage](https://perpulator.vercel.app)
- [ClawHub skill page](https://clawhub.ai/farisalahmad714/skills/perpulator)
- [Perpulator calculate API](https://perpulator.vercel.app/api/v1/calculate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown analysis with tables, risk notes, and error feedback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PERPULATOR_API_KEY and curl; sends user-provided trade parameters to an external API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
