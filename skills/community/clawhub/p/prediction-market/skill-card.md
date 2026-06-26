## Description: <br>
Helps agents read and participate in a Base mainnet garden temperature prediction market by checking market state and preparing HIGHER or LOWER ETH bet transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Potdealer](https://clawhub.ai/user/Potdealer) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to inspect the daily GTM market state, decide whether to bet HIGHER or LOWER on the 18:00 UTC garden temperature result, and prepare transaction payloads or commands for manual submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce ready-to-use Base mainnet betting transactions that spend ETH and may be irreversible. <br>
Mitigation: Use a separate low-balance wallet, verify every transaction field manually, and require explicit approval before submission. <br>
Risk: Raw private-key command examples can encourage unsafe handling of wallet credentials. <br>
Mitigation: Never paste a main wallet private key into chat, shared terminals, logs, or agent-managed shell sessions. <br>
Risk: The market depends on a trusted keeper to submit off-chain temperature readings for settlement. <br>
Mitigation: Review the contract address, market rules, keeper trust model, and current on-chain state independently before betting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Potdealer/prediction-market) <br>
- [Publisher profile](https://clawhub.ai/user/Potdealer) <br>
- [DailyTempMarket contract on Basescan](https://basescan.org/address/0xA3F09E6792351e95d1fd9d966447504B5668daF6) <br>
- [SensorNet contract on Basescan](https://basescan.org/address/0xf873D168e2cD9bAC70140eDD6Cae704Ed05AdEe0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON transaction objects, shell command examples, and JavaScript helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Base mainnet transaction payloads that spend ETH if submitted by the user or wallet tool.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
