## Description: <br>
Helps agents fetch Polymarket market data, detect probability-sum arbitrage candidates, and monitor opportunities with optional alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect Polymarket markets, produce JSON arbitrage reports, and run monitoring commands before making manual trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports a serious command-injection risk in the monitor script. <br>
Mitigation: Review and fix command construction before running the monitor, and avoid passing untrusted values to command-line options. <br>
Risk: The package under-discloses local execution, file writes, network access, and optional alerting behavior. <br>
Mitigation: Run only in a controlled environment after reviewing scripts, expected network destinations, output paths, and alert configuration. <br>
Risk: Arbitrage outputs may rely on stale homepage prices, low liquidity, or non-executable displayed probabilities. <br>
Mitigation: Treat results as screening signals only; manually verify prices, liquidity, fees, and market resolution terms before any trade. <br>
Risk: Webhook URLs can contain secrets or send sensitive alert data outside the local environment. <br>
Mitigation: Use non-secret test webhooks first, avoid embedding credentials in URLs when possible, and document alert payload contents before enabling alerts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guohongbin-git/polymarket-arbitrage-cn) <br>
- [Publisher Profile](https://clawhub.ai/user/guohongbin-git) <br>
- [ClawHub](https://clawhub.ai) <br>
- [Polymarket](https://polymarket.com) <br>
- [Polymarket Documentation](https://docs.polymarket.com) <br>
- [Arbitrage Types on Polymarket](references/arbitrage_types.md) <br>
- [Getting Started with Polymarket Arbitrage](references/getting_started.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes market scans, arbitrage results, and alert state under polymarket_data when scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
