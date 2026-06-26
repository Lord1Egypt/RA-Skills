## Description: <br>
Helps agents read OK Computer NFT data and build Bankr-compatible transactions for onchain messages, pages, Ring Gates transmissions, and Net Protocol storage on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[potdealer](https://clawhub.ai/user/potdealer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect OK Computers, compose onchain social messages and direct messages, manage token pages and usernames, and assemble or shard Ring Gates transmissions. It is intended for agents that need guidance, commands, JavaScript code, or transaction JSON for Base blockchain workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Onchain writes and signatures can create irreversible Base blockchain transactions. <br>
Mitigation: Use a limited wallet or API key, keep Base ETH exposure low, and inspect every transaction and signature request before submission. <br>
Risk: The Bankr API key can authorize transaction submission or signing through Bankr endpoints. <br>
Mitigation: Store BANKR_API_KEY only in the runtime environment, avoid sharing it in prompts or onchain data, and rotate it if exposed. <br>
Risk: The Net Protocol loader can execute content returned through a JSONP relay. <br>
Mitigation: Use the JSONP loader only with trusted relay content and avoid loading untrusted pages or scripts. <br>
Risk: Public onchain storage can expose messages, pages, and data permanently. <br>
Mitigation: Do not store private data, secrets, or sensitive content onchain. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/potdealer/ok-computers) <br>
- [OK Computers project site](https://okcomputers.xyz) <br>
- [Base blockchain](https://base.org) <br>
- [Net Protocol](https://netprotocol.app) <br>
- [Ring Gates protocol specification](RING-GATES.md) <br>
- [Agent skill guide](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript examples, shell commands, configuration notes, and JSON transaction objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Bankr-compatible transaction JSON for user review and submission; read-only operations produce formatted blockchain data.] <br>

## Skill Version(s): <br>
2.2.0 (source: ClawHub release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
