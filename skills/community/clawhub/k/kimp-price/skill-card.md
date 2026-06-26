## Description: <br>
Calculates the real-time Bitcoin Kimchi Premium by comparing BTC prices on Upbit and Binance using a live USD/KRW exchange rate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seungdols](https://clawhub.ai/user/seungdols) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and market-data users can run this skill to fetch live BTC prices and a USD/KRW exchange rate, then inspect the current Kimchi Premium as structured output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts third-party market-data APIs whenever it runs. <br>
Mitigation: Use it only in environments where outbound requests to the listed exchange-rate and exchange APIs are acceptable. <br>
Risk: The calculated premium is informational market data and may be incomplete, delayed, or unsuitable for financial decisions. <br>
Mitigation: Verify results against authoritative market sources and do not treat the output as financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seungdols/kimp-price) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON written to standard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes timestamp, USD/KRW exchange rate, Upbit BTC price, Binance BTC price, premium percentage, and KRW price difference.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
