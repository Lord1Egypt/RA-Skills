## Description: <br>
Accept crypto payments in AI agent conversations. Generate MetaMask/Trust Wallet deeplinks, verify transactions on-chain, check balances, issue receipts. No custody, no backend, no API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AmitayBohadana](https://clawhub.ai/user/AmitayBohadana) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and AI-agent builders use PayGents to request EVM payments, generate wallet deeplinks, verify transactions on-chain, check balances, and issue receipts without custodying private keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Malformed chain IDs can cause some scripts to run unintended local Node.js code. <br>
Mitigation: Use fixed known numeric chain IDs, avoid letting untrusted chat input choose script arguments, and review or patch the scripts before installation. <br>
Risk: Public RPC fallback endpoints can observe wallet addresses and transaction hashes queried by the skill. <br>
Mitigation: Configure trusted RPC endpoints with RPC_<chainId> environment variables or config.json when wallet privacy matters. <br>
Risk: A prefilled payment link can still present an incorrect recipient, token, chain, or amount to the user. <br>
Mitigation: Require the user to verify the recipient, token, chain, and amount in their wallet before approving any payment. <br>
Risk: Receipt output written with --out could be directed to an unintended location. <br>
Mitigation: Keep --out pointed at a dedicated receipt folder controlled by the user or agent runtime. <br>


## Reference(s): <br>
- [EVM Payment Deeplink Reference](references/evm-usdc-poc.md) <br>
- [PayGents ClawHub Release](https://clawhub.ai/AmitayBohadana/paygents) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, Markdown, wallet deeplink URLs, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces payment intents, wallet deeplinks, on-chain verification results, balance summaries, and receipts.] <br>

## Skill Version(s): <br>
0.3.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
