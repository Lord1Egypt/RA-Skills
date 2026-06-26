## Description: <br>
Provides lifelines-based survival analysis and Cox proportional hazards modeling guidance, including residual diagnostics, custom parametric regression, time-lagged conversion analysis, and proportional hazards checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to generate survival-analysis guidance and code for lifelines workflows such as Cox model diagnostics, parametric regression, conversion-rate survival modeling, and visualization. Because the artifact also contains ZVT trading and backtesting prompts, users should confirm the intended workflow before executing setup or market-data actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is labeled as lifelines survival analysis, but evidence.security reports repeated steering toward ZVT quant trading, backtesting, broker/provider use, and local setup. <br>
Mitigation: Use the skill only when that trading behavior is intended; otherwise restrict it to lifelines survival-analysis tasks and block trading, setup, and market-data execution paths. <br>
Risk: The artifact asks about data providers including paid accounts and broker-linked options, which can expose credentials or trigger unwanted paid/provider workflows. <br>
Mitigation: Do not provide broker, paid-provider, or trading credentials; keep any data collection or backtesting isolated and simulation-only. <br>
Risk: The evidence lists capabilities for crypto and purchase-capable behavior, increasing the impact of unintended execution. <br>
Mitigation: Require explicit user confirmation before shell commands, package setup, market-data access, or any workflow related to trading or purchasing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tangweigang-jpg/lifelines-survival-analysis) <br>
- [Human Summary](artifact/human_summary.md) <br>
- [Known Use Cases](artifact/references/USE_CASES.md) <br>
- [Component Capability Map](artifact/references/COMPONENTS.md) <br>
- [Semantic Locks and Preconditions](artifact/references/LOCKS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code and shell-command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for market, provider, strategy, and time-range parameters when following the ZVT trading path; no fixed output schema.] <br>

## Skill Version(s): <br>
0.3.3 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
