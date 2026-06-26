## Description: <br>
Compares Uniswap LP strategies for a token pair across versions, fee tiers, range widths, chains, APY, impermanent loss, gas costs, and risk ratings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and DeFi practitioners use this skill to compare viable LP strategies for a token pair before choosing whether and how to provide liquidity. It supports side-by-side evaluation of pool versions, fee tiers, range widths, rebalancing posture, APY, impermanent loss, gas costs, and qualitative risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LP strategy outputs may contain stale or inaccurate APY, impermanent loss, gas, pool, or risk estimates. <br>
Mitigation: Verify APY, impermanent loss, gas costs, pool data, and risk assumptions independently before acting on any recommendation. <br>
Risk: The skill can suggest moving from analysis to liquidity execution through other skills or agents. <br>
Mitigation: Review any subagent or execution skill separately, especially if it requests wallet access, API keys, or transaction authority. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/lp-strategy) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, analysis, guidance] <br>
**Output Format:** [Markdown or text with comparison tables and strategy notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces analysis only; it does not execute liquidity transactions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
