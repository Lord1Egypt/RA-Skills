## Description: <br>
Price options, compute Greeks, solve implied volatility, and generate payoff, option-chain, breakeven, and P/L tables in a terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and finance-oriented analysts use this skill for command-line Black-Scholes option pricing, Greeks, implied volatility, payoff, option-chain, breakeven, and position P/L calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted inputs can make the calculator run local code. <br>
Mitigation: Use only trusted, manually typed numeric inputs; maintainers should validate numeric arguments safely and pass values to Python without source interpolation. <br>
Risk: Pricing history may be stored automatically in $HOME/.option-calculator/history.log. <br>
Mitigation: Avoid entering sensitive pricing data unless local history retention is acceptable; maintainers should make history logging opt-in with clear delete and disable controls. <br>


## Reference(s): <br>
- [Option Calculator on ClawHub](https://clawhub.ai/xueyetianya/option-calculator) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Terminal text with numeric tables and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Price commands append calculation history to $HOME/.option-calculator/history.log.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
