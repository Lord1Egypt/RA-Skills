## Description: <br>
Multi-asset investment portfolio management framework with A/B/C asset-class differentiated rules, 7 red-line portfolio risk controls, and 4-factor QMS quality scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors and portfolio reviewers use Invassistant to structure multi-market portfolio checks, risk-control reviews, entry and exit decisions, and notification-ready investment reports. It supports US stocks, China A-shares, and Hong Kong stocks with differentiated strategy rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Investment guidance may be incorrect, stale, or unsuitable for the user's financial situation. <br>
Mitigation: Review the financial logic independently and require explicit human approval before acting on any recommendation. <br>
Risk: Optional webhook notifications may send holdings, prices, signals, and risk commentary to third-party chat platforms. <br>
Mitigation: Keep notification webhooks disabled unless the destination and data-sharing implications are understood and approved. <br>
Risk: Automating this skill into live trading could turn advisory output into financial execution without sufficient controls. <br>
Mitigation: Do not connect outputs directly to live trading systems without independent confirmation, access controls, and explicit approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/haiyangchenbj/invassistant) <br>
- [US Stock Strategy](references/us_stock_strategy.md) <br>
- [A-Share Strategy](references/a_share_strategy.md) <br>
- [Risk Control and Overrides](references/risk_control_and_overrides.md) <br>
- [Yahoo Finance Chart API](https://query1.finance.yahoo.com/v8/finance/chart/{symbol}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with optional Python-generated reports and notification payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory and require human review before trading or notification delivery.] <br>

## Skill Version(s): <br>
2.3.2 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
