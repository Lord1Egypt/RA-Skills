## Description: <br>
paynode-402 gives agents access to a dynamic premium API marketplace for real-time external tools through USDC micro-payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paynodelabs](https://clawhub.ai/user/paynodelabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover paid marketplace APIs, inspect required parameters and pricing, and execute approved paid requests for current data or specialized external services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign transactions and spend real USDC through paid API calls. <br>
Mitigation: Use a minimally funded burner wallet, review the API, price, and network before approval, and require explicit user confirmation before paid mainnet execution. <br>
Risk: Sensitive wallet credentials may be read from CLIENT_PRIVATE_KEY or the PayNode config fallback. <br>
Mitigation: Provide only a burner wallet key, restrict access to the config file, and verify ~/.config/paynode/config.json before activation. <br>
Risk: External CLI execution or unpinned updates can change behavior before real-value transactions. <br>
Mitigation: Pin the PayNode CLI version or locally audit and build the CLI before using real funds. <br>


## Reference(s): <br>
- [PayNode CLI homepage](https://github.com/PayNodeLabs/paynode-402-cli) <br>
- [PayNode CLI package](https://www.npmjs.com/package/@paynodelabs/paynode-402-cli) <br>
- [PayNode SDK](https://github.com/PayNodeLabs/paynode-sdk-js) <br>
- [PayNode protocol documentation](https://docs.paynode.dev) <br>
- [Base network faucets](https://docs.base.org/base-chain/network-information/network-faucets#network-faucets) <br>
- [ClawHub skill page](https://clawhub.ai/paynodelabs/paynode-402) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bun, CLIENT_PRIVATE_KEY or the PayNode config file, and explicit approval before spending real USDC.] <br>

## Skill Version(s): <br>
2.7.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
