## Description: <br>
A Polymarket prediction-market arbitrage skill that scans markets, identifies apparent price deviations, and can submit live trades with per-call billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BOB-Z-PRO](https://clawhub.ai/user/BOB-Z-PRO) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to scan Polymarket markets for apparent arbitrage opportunities and, when configured with a Polygon private key, submit live buy orders from the CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Polygon wallet private key and can use it to sign live trading orders. <br>
Mitigation: Use only a dedicated low-balance wallet, never a primary wallet, and review private-key handling before installing or running the skill. <br>
Risk: The scan and monitoring commands may place live orders automatically when wallet credentials are configured. <br>
Mitigation: Confirm the command behavior before use, prefer a dry-run or manual-confirmation version, and set hard spend limits outside the skill. <br>
Risk: The security evidence flags unclear safeguards around automatic trading and sensitive wallet access. <br>
Mitigation: Review the code and dependencies carefully, test with minimal funds, and avoid unattended operation until safeguards are confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BOB-Z-PRO/polymarket-arbitrage-pro) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [CLI console text with market summaries, opportunity reports, order status, wallet balance, and billing status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate live Polymarket API orders and SkillPay billing when the required environment variables are configured.] <br>

## Skill Version(s): <br>
7.1.5 (source: server release metadata; artifact frontmatter reports 7.1.4 and package.json reports 7.1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
