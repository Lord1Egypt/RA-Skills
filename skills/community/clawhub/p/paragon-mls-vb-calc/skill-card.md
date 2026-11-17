## Description:

Compare amortized debt, extra payments, chunking/basic acceleration, and advanced velocity banking for a real estate deal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earlvanze](https://clawhub.ai/user/earlvanze)

### License/Terms of Use:

MIT-0

## Use Case:

Real estate deal analysts and operators use this skill to compare standard amortization, extra payments, chunking/basic acceleration, and advanced velocity banking strategies before choosing a debt payoff approach. It supports decision-making only and is not lending advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on local external Node.js MCP code and npm dependencies that are not included in the reviewed artifact.

Mitigation: Install only after separately reviewing the external paragon-mls-mcp workspace, lockfile, dependencies, and built dist/index.js.

Risk: Debt strategy outputs can be misleading when based on incomplete or inaccurate property income, expense, interest rate, or HELOC assumptions.

Mitigation: Use actual property or operator budget values and treat the result as decision support, not lending advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/earlvanze/skills/paragon-mls-vb-calc)
- [ClawHub publisher profile](https://clawhub.ai/user/earlvanze)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, comparison tables, and JSON-shaped calculator results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill expects numeric debt, income, expense, rate, limit, and chunking inputs for the MCP calculator.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
