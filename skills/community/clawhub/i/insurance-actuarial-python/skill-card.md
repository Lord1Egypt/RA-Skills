## Description: <br>
Helps agents produce Python-oriented guidance and code for actuarial interest-rate analysis, including SSA time-series decomposition, stationary bootstrap inference, yield curve fitting, and derivative calibration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, quantitative analysts, and actuarial practitioners use this skill to generate Python workflows for actuarial and interest-rate modeling tasks such as SSA decomposition, bootstrap inference, NSS curve fitting, and calibration examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the skill is advertised for actuarial interest-rate modeling but its files also steer agents toward stock and crypto trading workflows and persistent setup. <br>
Mitigation: Review generated plans and code before execution, and treat trading-related outputs as requiring explicit user approval. <br>
Risk: The release security guidance warns against connecting broker accounts, paid data-provider credentials, wallets, or live trading access without review. <br>
Mitigation: Use an isolated Python environment and require separate per-action approval before connecting financial accounts, credentials, wallets, or live trading systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/insurance-actuarial-python) <br>
- [Human Summary](artifact/human_summary.md) <br>
- [Known Use Cases](artifact/references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](artifact/references/LOCKS.md) <br>
- [Component Capability Map](artifact/references/COMPONENTS.md) <br>
- [Anti-Patterns](artifact/references/ANTI_PATTERNS.md) <br>
- [Cross-Project Wisdom](artifact/references/WISDOM.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for market, data provider, strategy type, time range, and target entity IDs before producing workflows.] <br>

## Skill Version(s): <br>
0.3.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
