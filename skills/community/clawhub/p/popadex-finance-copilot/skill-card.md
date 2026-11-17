## Description:

Read-only personal finance copilot for net worth insights, account allocation, salary and tax comparisons across countries, disposable-income rankings, retirement projections, budget Sankey data, and portfolio value, performance, history, and CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bit-of-a-shambles](https://clawhub.ai/user/bit-of-a-shambles)

### License/Terms of Use:

MIT-0

## Use Case:

External PopaDex users use this skill to ask an agent for read-only analysis of net worth, account allocation, tax and salary scenarios, retirement readiness, budgets, and portfolio history. The skill depends on a compatible PopaDex MCP server exposing read-only finance tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads financial summaries and portfolio data through a PopaDex MCP server.

Mitigation: Install only if the publisher and MCP server are trusted, keep access read-only, and avoid exposing secrets or private tokens.

Risk: Salary, tax, retirement, and portfolio outputs may be mistaken for regulated financial or investment advice.

Mitigation: Clearly label estimates and assumptions, show formulas where useful, avoid guaranteed-return claims, and direct users to qualified professionals for regulated advice.

Risk: Missing or stale inputs can make projections and comparisons misleading.

Mitigation: Ask for required inputs explicitly and state confidence levels before providing recommendations.

## Reference(s):

- [PopaDex](https://popadex.com)
- [PopaDex Help](https://app.popadex.com/help)
- [ClawHub Skill Page](https://clawhub.ai/bit-of-a-shambles/skills/popadex-finance-copilot)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or plain text with estimates, assumptions, concise recommendations, optional next actions, and CSV content when export is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be treated as estimates and not regulated financial or investment advice.]

## Skill Version(s):

0.1.1 (source: server release evidence and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
