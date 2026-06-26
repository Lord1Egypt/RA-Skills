## Description: <br>
Send and receive encrypted on-chain messages on the Kaspa blockchain using the Kasia protocol. Use when a user asks to message someone on Kaspa/Kasia, check Kasia conversations, read encrypted messages, send payments with messages, or manage Kasia handshakes. Requires kasia-mcp and kaspa-mcp servers configured in mcporter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renkasiyas](https://clawhub.ai/user/renkasiyas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Kaspa users use this skill to manage Kasia conversations, encrypted messages, handshakes, self-stash data, and message-linked payments through configured kasia-mcp and kaspa-mcp tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet seed material and local decrypted-message or configuration data. <br>
Mitigation: Use a dedicated low-balance wallet, avoid passing a primary mnemonic on the command line, and lock down or avoid plaintext mcporter secret storage. <br>
Risk: Write operations produce mainnet transaction payloads that can spend KAS when broadcast. <br>
Mitigation: Manually review every generated payload, recipient, amount, and message before broadcasting with kaspa-mcp. <br>
Risk: The skill depends on external kasia-mcp and kaspa-mcp code. <br>
Mitigation: Review the external MCP server code before installation and only run trusted builds. <br>


## Reference(s): <br>
- [Kasia Protocol Reference](references/protocol.md) <br>
- [Kasia Indexer API](https://indexer.kasia.fyi) <br>
- [ClawHub Skill Page](https://clawhub.ai/renkasiyas/kasia) <br>
- [Publisher Profile](https://clawhub.ai/user/renkasiyas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-like tool payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction payloads and broadcast instructions for separate user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
