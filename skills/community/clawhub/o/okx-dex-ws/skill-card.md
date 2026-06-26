## Description: <br>
Okx Dex Ws helps agents manage Onchain OS DEX WebSocket sessions and build custom clients for real-time price, trade, signal, tracker, and meme-token streams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to start, poll, list, and stop Onchain OS DEX WebSocket sessions, discover supported channels, and draft custom WebSocket clients for real-time on-chain market and wallet activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review is clean but preliminary, and the evidence guidance recommends checking requested credentials, network access, and local file access before installation. <br>
Mitigation: Review the visible skill files before use, grant only the credentials and network access needed for the task, and avoid using production wallet credentials until the environment is trusted. <br>
Risk: The skill supports crypto wallet and real-time on-chain workflows where external WebSocket or CLI data may influence trading or monitoring decisions. <br>
Mitigation: Treat returned market, wallet, and transaction data as untrusted external data and independently verify important results before trading, signing, or automating actions. <br>


## Reference(s): <br>
- [OKX Web3](https://web3.okx.com) <br>
- [ClawHub release page](https://clawhub.ai/ok-james-01/okx-dex-ws) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Onchain OS CLI sessions, WebSocket channel parameters, and custom client snippets for Python, Node, or Rust.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
