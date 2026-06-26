## Description: <br>
Track and compare product prices across popular Indian stores (Amazon India, Flipkart, Reliance Digital, Croma, Vijay Sales, Tata CLiQ, and more), compute effective prices after offers/cashback, detect arbitrage opportunities, and monitor price history with alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anugotta](https://clawhub.ai/user/anugotta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and price analysts use this skill to compare India-focused ecommerce prices, calculate effective payable costs, monitor price history, and flag price-drop or arbitrage opportunities for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live store integrations can violate platform terms, rate limits, or regional legal requirements if enabled without review. <br>
Mitigation: Keep the default mock mode for local evaluation and move to live adapters only after store policy review, rate-limit planning, and legal or compliance sign-off. <br>
Risk: Price, stock, shipping, cashback, and SKU matching data can be incomplete or misleading. <br>
Mitigation: Treat outputs as decision support, include confidence notes, flag uncertain matches, and manually verify high-value opportunities before purchases or resale decisions. <br>
Risk: Credential exposure is possible if live adapters are extended with API keys. <br>
Mitigation: Do not hardcode API keys in source code or chat, and review any live adapter changes before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anugotta/india-price-tracker) <br>
- [OpenClaw homepage metadata](https://clawhub.ai/Michael-laffin/price-tracker) <br>
- [README](README.md) <br>
- [Setup](setup.md) <br>
- [Validation checklist](validation-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default scripts use mock adapters; generated reports are decision support and should be manually verified before high-value action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
