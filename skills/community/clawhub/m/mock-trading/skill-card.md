## Description: <br>
Simulate cryptocurrency trading using algorithmic strategies (SMA Crossover, Mean Reversion) without risking real capital. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yadavabhijeet4](https://clawhub.ai/user/yadavabhijeet4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run local paper-trading simulations, test simple crypto strategy logic, and report cash balance, position value, PnL, and trade history from a mock portfolio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill updates a portfolio JSON file selected by the user. <br>
Mitigation: Use a dedicated portfolio filename and avoid pointing the script at important files. <br>
Risk: The skill contacts CoinGecko for public cryptocurrency price data. <br>
Mitigation: Run it only in environments where outbound access to that public API is acceptable. <br>
Risk: Heartbeat or cron scheduling can make the mock trading script run repeatedly. <br>
Mitigation: Add scheduling only when the operator knows how to disable or remove it later. <br>


## Reference(s): <br>
- [Mock Trading on ClawHub](https://clawhub.ai/yadavabhijeet4/mock-trading) <br>
- [CoinGecko simple price endpoint](https://api.coingecko.com/api/v3/simple/price?ids={asset_id}&vs_currencies=usd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON portfolio updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local portfolio JSON file and public CoinGecko price data; no API keys are indicated by the evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
