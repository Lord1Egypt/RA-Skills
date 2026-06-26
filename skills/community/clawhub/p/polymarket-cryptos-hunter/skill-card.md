## Description: <br>
Runs an HFT market-making bot for Polymarket with live execution through Web3 and the CLOB API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thony32](https://clawhub.ai/user/thony32) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who intentionally operate Polymarket trading automation use this skill to start a continuous market-making bot for crypto up/down markets with live wallet and CLOB connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous live-money trading can place orders and affect a funded wallet without step-by-step user approval. <br>
Mitigation: Review the code, wallet setup, position sizing, risk limits, and stop procedure before installation; prefer paper trading or a dry-run environment first. <br>
Risk: The artifact is designed to run continuously in the background, which can reduce operator visibility while the process is active. <br>
Mitigation: Run only when the process can be monitored and stopped promptly, and avoid loading private keys or funded wallets unless active supervision is available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thony32/polymarket-cryptos-hunter) <br>
- [Publisher profile](https://clawhub.ai/user/thony32) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing instructions for starting a continuous background trading process.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
