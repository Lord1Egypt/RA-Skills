## Description: <br>
Trade prediction markets using LLM probability estimation enriched with real-time data sources, then act when the estimate diverges from the market price. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mibayy](https://clawhub.ai/user/Mibayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and prediction-market operators use this skill to run a configurable estimator that gathers public market context, asks an LLM for probability estimates, and optionally places trades through Simmer/Polymarket when configured thresholds are met. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make repeated automated financial trading decisions when live mode and a real trading venue are enabled. <br>
Mitigation: Keep the skill in dry-run or simulated venue mode until the source, dependencies, trade size, venue, thresholds, and operational limits have been reviewed and approved. <br>
Risk: LLM probability estimates and public data sources can be wrong, stale, incomplete, or overconfident. <br>
Mitigation: Use conservative thresholds, monitor logs and trade outcomes, cap LLM calls and trade size, and require human review before enabling live trading. <br>
Risk: The configured LLM endpoint and external APIs receive market questions and public context during estimation. <br>
Mitigation: Use trusted providers, protect API keys, review endpoint configuration, and avoid adding private or sensitive data to market prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mibayy/polymarket-multi-source-estimator) <br>
- [Publisher profile](https://clawhub.ai/user/Mibayy) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with shell commands, environment variable configuration, runtime logs, LLM probability estimates, and optional trading API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a scheduled managed automaton by default; dry-run unless live trading is explicitly enabled.] <br>

## Skill Version(s): <br>
1.1.4 (source: release evidence, artifact metadata, and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
