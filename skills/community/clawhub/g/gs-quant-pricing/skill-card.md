## Description: <br>
Provides quantitative finance assistance for annualized volatility, exponential moving averages, exponentially weighted standard deviation, financial time-series analysis, and asset-pricing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative finance practitioners use this skill to ask an agent for indicator calculations, ZVT-based data workflows, backtesting code, trading-signal logic, and analysis guidance for A-share, HK, or crypto scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents a pricing-indicator purpose but can steer agents toward broader finance workflows, including data fetching, backtesting, trading-order logic, local setup, and write-capable analytics references. <br>
Mitigation: Review generated commands before execution and keep the skill away from live brokerage, paid provider, portfolio, entitlement, or risk-model upload access unless each action is explicitly authorized. <br>
Risk: Generated trading or backtesting guidance can be misleading if it violates the artifact's execution constraints, such as next-bar execution, T+1 handling, signal-column semantics, or required DataFrame indexing. <br>
Mitigation: Validate generated code against the semantic locks and preconditions in the reference files before using it for financial analysis or trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/gs-quant-pricing) <br>
- [Human Summary](human_summary.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Constraints](references/CONSTRAINTS.md) <br>
- [Authoritative Seed](references/seed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated finance-analysis code, setup commands, data-provider choices, backtest steps, and warnings about execution constraints.] <br>

## Skill Version(s): <br>
0.3.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
