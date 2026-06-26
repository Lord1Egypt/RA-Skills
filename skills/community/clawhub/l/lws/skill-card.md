## Description: <br>
Lightweight Wallet Signer CLI for generating wallets, deriving addresses, and signing messages across EVM, Solana, Bitcoin, Cosmos, and Tron chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[njdawn](https://clawhub.ai/user/njdawn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate a local wallet-signing CLI for test or local wallet workflows across multiple blockchain networks. It covers generating mnemonics, deriving addresses, signing messages, listing stored wallet descriptors, updating the tool, and uninstalling it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The one-line installer downloads and executes a remote shell script. <br>
Mitigation: Inspect the installer and pin the source before installation, or build from reviewed source instead. <br>
Risk: Mnemonic phrases passed as command-line arguments can be exposed through shell history or process inspection. <br>
Mitigation: Use test wallets, avoid funded-wallet seed phrases, and prefer workflows that pass secrets through a safer prompt, stdin, keychain, or hardware wallet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/njdawn/lws) <br>
- [Project homepage](https://github.com/dawnlabsai/lws) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target macOS and Linux and require git and cargo.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
