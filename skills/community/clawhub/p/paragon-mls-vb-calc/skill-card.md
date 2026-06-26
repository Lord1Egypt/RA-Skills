## Description: <br>
Compares amortized debt, extra payments, chunking/basic acceleration, and advanced velocity banking for a real estate deal to help decide whether chunking or advanced VB makes sense for a property. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earlvanze](https://clawhub.ai/user/earlvanze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Real estate deal analysts, operators, and agents use this skill to compare debt payoff strategies, estimate interest savings and payoff timing, and decide whether HELOC-based chunking or advanced velocity banking fits a property. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run unreviewed external Node/MCP code from a host-specific path and execute npm install/build scripts outside the packaged skill. <br>
Mitigation: Install only after inspecting the referenced paragon-mls-mcp project, its npm dependencies, and its build scripts on the host. <br>
Risk: The skill may process confidential income, expense, debt, HELOC, or other financial details. <br>
Mitigation: Avoid entering sensitive financial data until the local MCP implementation and its data handling behavior are trusted. <br>
Risk: Velocity banking and HELOC comparisons can be mistaken for lending advice or relied on with inaccurate assumptions. <br>
Mitigation: Treat results as decision support, use actual property or operator budget numbers, and review recommendations before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earlvanze/paragon-mls-vb-calc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown comparison table with JSON details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include debt payoff comparisons, savings versus baseline, and a recommendation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
