## Description: <br>
End-to-end OpenBytes network API workflows for AI agents, covering wallet signature authentication, on-chain top-up checks, consumer API key lifecycle operations, model inference through the gateway, and balance and usage queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viyozc](https://clawhub.ai/user/viyozc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate or debug OpenBytes API workflows, including wallet login, API key management, top-up verification, model requests, balance checks, usage review, and parent-wallet connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet private keys, session tokens, API keys, signatures, authorization headers, and personal data may be exposed if an agent generates, prints, stores, or receives secrets during troubleshooting. <br>
Mitigation: Use a trusted wallet for signing, keep private keys outside the agent, store API keys in secret managers or environment variables, and redact secrets from logs and shared outputs. <br>
Risk: Incorrect gateway URLs, contract addresses, chain IDs, parent-wallet relationships, transaction amounts, approvals, deposits, API-key creation, or revocation can affect funds or account access. <br>
Mitigation: Manually verify these values against trusted sources before executing commands or transactions, and review every generated curl command before running it. <br>


## Reference(s): <br>
- [OpenBytes gateway API](https://gateway.openbytes.ai) <br>
- [ethers.js Wallet.createRandom documentation](https://docs.ethers.org/v6/api/wallet/#Wallet-createRandom) <br>
- [viem createWallet documentation](https://viem.sh/docs/actions/wallet/createWallet.html) <br>
- [Base Sepolia RPC endpoint](https://sepolia.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell, JavaScript, TypeScript, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions and example HTTP requests; users must supply their own wallet, token, API key, chain, and endpoint values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
