## Description: <br>
Interact with the Mutinynet Bitcoin testnet faucet to get testnet bitcoin on-chain, pay Lightning invoices, open Lightning channels, and generate BOLT11 invoices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benthecarman](https://clawhub.ai/user/benthecarman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Bitcoin/Lightning testers use this skill to install and run the Mutinynet faucet CLI for signet/testnet funding, Lightning payments, channel setup, and BOLT11 invoice generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored faucet tokens can grant access to a local Mutinynet faucet session if exposed. <br>
Mitigation: Treat ~/.mutinynet/token and MUTINYNET_FAUCET_TOKEN as credentials, and remove the stored token when the session is no longer needed. <br>
Risk: Payment and channel commands can send testnet funds or open channels to unintended destinations if inputs are wrong. <br>
Mitigation: Verify invoices, addresses, peer pubkeys, hosts, and amounts before running commands, and keep the default faucet URL unless another endpoint is trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/benthecarman/mutinynet-cli) <br>
- [Project repository metadata](https://github.com/benthecarman/mutinynet-cli) <br>
- [GitHub releases](https://github.com/benthecarman/mutinynet-cli/releases/latest) <br>
- [Mutinynet](https://mutinynet.com) <br>
- [Mutinynet faucet](https://faucet.mutinynet.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include installation and command guidance for a Rust CLI that uses network access and stores a local faucet token.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release, SKILL.md frontmatter, Cargo.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
