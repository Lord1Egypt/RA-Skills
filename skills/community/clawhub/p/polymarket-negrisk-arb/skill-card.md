## Description: <br>
Scan multi-outcome Polymarket markets for mathematical arbitrage and optionally execute simultaneous batch trades when summed outcome prices fall below configured thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[r2crypto](https://clawhub.ai/user/r2crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill to scan multi-outcome Polymarket-style markets for NegRisk price-sum arbitrage, tune thresholds, and run dry-run or live Simmer/Polymarket batch execution workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place scheduled live trades quietly when configured with a Simmer API key. <br>
Mitigation: Start in dry-run mode, keep live automaton execution disabled until reviewed, and use a narrowly scoped or low-balance API key. <br>
Risk: Batch trades can partially fail or execute after prices move, which can reduce or remove the expected arbitrage. <br>
Mitigation: Monitor fills and the ledger after each run, keep position and daily budget caps low, and review slippage and fee settings before live use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/r2crypto/polymarket-negrisk-arb) <br>
- [Publisher profile](https://clawhub.ai/user/r2crypto) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text with optional JSON output, configuration values, and local ledger/status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run scan output is available by default; live mode can submit batch trades when configured with a Simmer API key.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata, SKILL.md frontmatter, and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
