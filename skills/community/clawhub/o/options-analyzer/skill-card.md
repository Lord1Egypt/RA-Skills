## Description: <br>
Options Analyzer helps agents retrieve options-chain data, calculate Greeks, analyze implied volatility, evaluate multi-leg options strategies, and recommend strategies from a market outlook and risk posture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BENZEMA216](https://clawhub.ai/user/BENZEMA216) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to inspect public options data, compute option sensitivities, compare volatility metrics, and draft options-strategy analyses or recommendations. It is best suited for decision-support workflows where a human reviews market assumptions before acting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Options data and strategy recommendations may be incomplete, delayed, or unsuitable for a user's financial situation. <br>
Mitigation: Treat outputs as decision support only, verify market data and assumptions independently, and require human review before any real-money options trade. <br>
Risk: Dependency installation may fail or use unexpected package versions because scipy is required by the scripts but is not listed in the quick-start install command. <br>
Mitigation: Install the skill in an isolated virtual environment, pin and verify dependencies, and include scipy before running the analysis scripts. <br>


## Reference(s): <br>
- [Options Analyzer ClawHub Release](https://clawhub.ai/BENZEMA216/options-analyzer) <br>
- [strategies.md](references/strategies.md) <br>
- [greeks_guide.md](references/greeks_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON from command-line Python scripts, with example shell commands and strategy guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public market data through yfinance; outputs should be reviewed before financial decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
