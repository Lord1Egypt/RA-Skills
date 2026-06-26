## Description: <br>
Kelly Formula Crypto helps agents calculate cryptocurrency position sizes using Kelly Criterion, fractional Kelly, multi-strategy allocation, and leverage safety checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinboh68-prog](https://clawhub.ai/user/jinboh68-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading-focused agents use this skill to compute Kelly-based cryptocurrency position sizes, fractional Kelly recommendations, multi-strategy allocation adjustments, and leverage safety checks. The outputs are decision-support guidance for risk management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises a 0.01 USDC x402 payment per call, so repeated autonomous invocations can incur charges. <br>
Mitigation: Confirm each wallet or payment prompt and set invocation limits before using the skill in automated workflows. <br>
Risk: Calculation inputs may be sent to the disclosed hosted endpoint. <br>
Mitigation: Avoid submitting sensitive trading strategy details unless the endpoint and data handling are acceptable for the intended use. <br>
Risk: Kelly position sizing depends on estimated win probability, payout ratio, losses, fees, and market conditions. <br>
Mitigation: Treat outputs as decision-support, account for fees and slippage, and review recommendations before placing trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinboh68-prog/kelly-formula-crypto) <br>
- [Hosted calculation endpoint](https://kelly-formula-crypto.vercel.app/api/calculate) <br>
- [x402 payment endpoint](https://api.x402.dev/pay) <br>
- [Original article referenced by the skill](https://x.com/KKaWSB/status/1968453490084299020) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON calculation results with position sizing and leverage safety guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a 0.01 USDC x402 payment per call and may send calculation inputs to the hosted endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
