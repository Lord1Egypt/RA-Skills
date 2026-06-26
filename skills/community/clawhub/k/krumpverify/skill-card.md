## Description: <br>
Enables AI agents (e.g. OpenClaw) to understand and use Krump Verify for on-chain move verification against Story IP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arunnadarasa](https://clawhub.ai/user/arunnadarasa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to verify dance moves against registered Story IP assets on Story Aeneid and to navigate USDC.k or x402/EVVM payment flows. It also helps developers understand the contract calls, receipt flow, relayer setup, and deployment references used by Krump Verify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent use can involve token approvals, EVVM deposits, x402 signatures, receipt consumption, deployments, or contract transactions that move value or alter on-chain state. <br>
Mitigation: Use a dedicated low-balance wallet and dedicated relayer key, verify contract addresses and fees, and require manual approval before any payment, signature, deployment, receipt use, or transaction. <br>
Risk: Incorrect EVVM/x402 payloads, nonces, executor settings, or unfunded EVVM balances can cause failed payment flows or unusable receipts. <br>
Mitigation: Confirm the sync nonce, zero executor, expected payload shape, receipt payer, receipt amount, and EVVM balance before submitting or using receipts. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/arunnadarasa/krumpverify) <br>
- [Publisher profile](https://clawhub.ai/user/arunnadarasa) <br>
- [ClawHub](https://clawhub.ai/) <br>
- [Story Aeneid explorer](https://aeneid.storyscan.io) <br>
- [Story Aeneid RPC](https://aeneid.storyrpc.io) <br>
- [Krump x402 relayer](https://krump-x402-relayer.fly.dev) <br>
- [EVVM/x402 Story Aeneid build guide](docs/BUILDING_WITH_EVVM_X402_STORY_AENEID.md) <br>
- [Deploy guide](DEPLOY.md) <br>
- [KrumpVerify contract](src/KrumpVerify.sol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline contract calls, addresses, environment variables, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing guidance for blockchain verification and payment workflows; execution should remain subject to user approval.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
