## Description: <br>
Randomly finds a live Polymarket politics market, checks trading context, and buys 1 USDC by default with explicit dry-run and live modes for AION Market. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssj124](https://clawhub.ai/user/ssj124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill as a minimal AION-compatible template for discovering politics markets on Polymarket, checking context, and running a dry-run or explicitly live 1 USDC trade. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for wallet-control credentials and can execute Polymarket trades when live mode is enabled. <br>
Mitigation: Use a dedicated low-balance wallet, keep the default dry-run mode for initial checks, and enable --live only after confirming the selected account, market, side, and amount. <br>
Risk: The release evidence reports under-disclosed recurring automation and redemption behavior. <br>
Mitigation: Review the managed cron behavior before installation, and do not use --auto-redeem unless the operator has confirmed the exact account actions and spending limits. <br>
Risk: The authoritative security verdict is suspicious because the skill combines sensitive credentials with trading automation. <br>
Mitigation: Review the skill before installing, trust the runtime and dependencies before providing a private key, and monitor all live executions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ssj124/polymarket-politics-random-buyer) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Operator text summary with optional JSON trade result and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AION API credentials and a wallet private key; defaults to dry-run unless --live is passed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
