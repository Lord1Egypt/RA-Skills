## Description: <br>
Launch a token on Flap BNB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flapguy](https://clawhub.ai/user/flapguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and token launch operators use this skill to collect token parameters, upload public token metadata, mine a vanity CREATE2 salt, and construct the BNB Chain transaction needed to launch a Flap token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill constructs and submits BNB Chain transactions, so incorrect contract addresses, calldata, chain ID, value, or gas settings can cause loss of funds or unintended token launches. <br>
Mitigation: Verify Flap contract addresses from official sources and review chainId, to, value, data, and gas in a trusted wallet before signing. <br>
Risk: Wallet signing can expose private keys or signing authority if handled through ad hoc scripts or untrusted tooling. <br>
Mitigation: Use a trusted wallet, hardware wallet, browser wallet, or MPC signer, and never paste private keys into temporary scripts or prompts. <br>
Risk: Token images and metadata uploaded through the Flap upload API can become public on IPFS. <br>
Mitigation: Only upload images and metadata that are safe to publish permanently. <br>


## Reference(s): <br>
- [Flap Documentation](https://docs.flap.sh) <br>
- [Preflight Checks](references/preflight.md) <br>
- [Vault Factory Setup](references/vault-factory.md) <br>
- [Token Metadata Upload](references/meta-upload.md) <br>
- [Tax Token Parameters](references/tax-params.md) <br>
- [Finding the Vanity Salt](references/salt-finding.md) <br>
- [Construct the EVM Transaction](references/construct-tx.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Constructs transaction details for external wallet review and signing; metadata uploads return an IPFS CID.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
