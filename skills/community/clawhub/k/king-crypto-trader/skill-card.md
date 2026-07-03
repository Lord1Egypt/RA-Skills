## Description: <br>
Crypto Trader provides automated cryptocurrency market scanning and Gate.io-oriented futures trading commands for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-focused agents can use this skill to request crypto market scans, status checks, and trading-signal output. Live use should be gated by exchange-key permissions, explicit approval, and portfolio risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous leveraged futures trading can create financial loss if connected to live exchange credentials without safeguards. <br>
Mitigation: Start with paper trading or read-only exchange keys, require explicit approval for live trades, and enforce hard position, leverage, and drawdown limits. <br>
Risk: The package delegates behavior to an unbundled local trading engine, so the complete trading logic is not visible in the packaged files. <br>
Mitigation: Review the external engine and its dependencies before installation or execution, and confirm it cannot place live trades outside the approved workflow. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kingaiwork/king-crypto-trader) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market scan counts, status text, and truncated signal output from the local trading engine.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
