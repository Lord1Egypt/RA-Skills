## Description: <br>
Tracks active Polymarket markets by total trading volume and prints market names, estimated Yes/No volume, current odds, and volume rankings, with skillpay.me payment required for normal runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ariesdevil](https://clawhub.ai/user/ariesdevil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to run a paid command-line report of high-volume active Polymarket markets, including odds and estimated Yes/No volume. Results are best used for market monitoring and should be verified before trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal runs can charge 0.001 USDT through skillpay.me. <br>
Mitigation: Use the balance-check path before running, review billing terms, and run only when the user accepts the charge. <br>
Risk: The report can present lifetime or estimated volume as recent market flow. <br>
Mitigation: Label results as total-volume rankings and rough Yes/No estimates, and verify against source market data before trading decisions. <br>
Risk: The skill depends on third-party billing and market-data endpoints. <br>
Mitigation: Install only when the user trusts skillpay.me and is comfortable sending requests to the referenced external services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ariesdevil/polymarket-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/ariesdevil) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [skillpay.me billing service](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text market ranking report with command-line status and billing messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns top 10 active markets by total volume; Yes/No volume split is estimated from outcome prices.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
