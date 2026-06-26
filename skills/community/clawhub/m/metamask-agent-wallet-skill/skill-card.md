## Description: <br>
Control a sandboxed MetaMask browser extension wallet for autonomous blockchain transactions. Features configurable permission guardrails including spend limits, chain allowlists, protocol restrictions, and approval thresholds. MetaMask-only (other wallets not supported). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreolf](https://clawhub.ai/user/andreolf) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to let an agent operate a dedicated MetaMask wallet for dapp connections, swaps, token transfers, message signing, balance checks, and transaction history review under configured wallet constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks users to run npm setup code and rely on unverified guardrails for irreversible crypto actions. <br>
Mitigation: Review the full source, package scripts, lockfile, and permission enforcement before installing, running setup, or trusting advertised spend limits. <br>
Risk: Automated wallet actions can move funds or sign messages through MetaMask. <br>
Mitigation: Use only a brand-new MetaMask wallet with very small funds, and never use a main wallet or seed phrase. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples, JSON configuration snippets, and transaction or approval summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet balances, transaction history, approval requests, and transaction outcomes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
