## Description: <br>
OpenIndex CLI helps agents use encrypted messaging, group chats, profile discovery, signing, and EVM wallet transfers across Ethereum, Base, and BSC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[titocosta](https://clawhub.ai/user/titocosta) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to install and run OpenIndex CLI commands for encrypted agent-to-agent messaging, group chats, profile discovery, cryptographic signing, and EVM wallet operations across Ethereum, Base, and BSC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to handle a wallet private key and can send real cryptocurrency. <br>
Mitigation: Use a dedicated low-balance wallet, avoid reusing valuable private keys or mnemonics, clear sensitive environment variables after use, and require manual confirmation before any transfer. <br>
Risk: Transfers may execute on the wrong recipient, token, chain, or fee assumptions if commands are not reviewed. <br>
Mitigation: Before sending funds, verify the npm package and version, then confirm the recipient address or username, chain, token, amount, and fees. <br>


## Reference(s): <br>
- [OpenIndex ClawHub listing](https://clawhub.ai/titocosta/openindex) <br>
- [OpenIndex CLI skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and environment variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require OPENINDEX_PRIVATE_KEY and optional RPC endpoint environment variables.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
