## Description: <br>
Automates paper-mode by default, and explicitly enabled live, Polymarket trading for Web3, DeFi, NFT, metaverse, robotics, quantum computing, and synthetic biology prediction markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and developers use this skill to discover emerging-technology Polymarket markets, apply configurable risk filters, and place simulated trades by default. Live trading is available only when deliberately run with live mode and valid Simmer credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated live trading can place real Polymarket orders when live mode is deliberately enabled with credentials. <br>
Mitigation: Keep the skill in paper mode unless live trading is intended, and use a least-privileged Simmer API key where available. <br>
Risk: The simmer-sdk dependency is not pinned in the artifact. <br>
Mitigation: Review and pin the dependency before providing live-capable credentials in an audited environment. <br>
Risk: Unattended execution can repeatedly evaluate markets and submit orders if scheduling is enabled. <br>
Mitigation: Confirm cron, autostart, and Simmer scheduling settings before enabling unattended runs. <br>
Risk: Emerging-technology prediction markets can be volatile or illiquid. <br>
Mitigation: Tune maximum position size, volume, spread, days-to-resolution, and open-position limits before trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-emerging-tech-trader) <br>
- [DeFiLlama](https://defillama.com/) <br>
- [IBM Quantum Network](https://quantum.ibm.com/) <br>
- [The Good Food Institute](https://gfi.org/) <br>
- [CoinGlass NFT](https://www.coinglass.com/nft) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk source](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Console text plus Simmer and Polymarket trade requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live trading requires --live and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata; artifact frontmatter says 1.0 and clawhub.json says 0.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
