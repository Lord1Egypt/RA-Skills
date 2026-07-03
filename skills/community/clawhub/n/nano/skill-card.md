## Description: <br>
Nano (XNO) cryptocurrency wallet operations, transaction analysis, and explorer lookups. Use for send/receive, balances, pending funds, address validation, unit conversion, tx/hash/account lookup, explorer links, and Nano block-lattice questions. Prefer xno-mcp first; use xno-skills CLI as fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cbrunnkvist](https://clawhub.ai/user/cbrunnkvist) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent work with Nano/XNO wallets, balances, sends, receives, address validation, unit conversion, QR requests, transaction history, representative changes, and explorer lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a Nano/XNO wallet and may initiate irreversible sends. <br>
Mitigation: Review wallet names, destination addresses, amounts, representative changes, and send confirmations before allowing execution. <br>
Risk: Balance checks may automatically receive pending Nano funds and update wallet state. <br>
Mitigation: Use the skill only when wallet state changes are expected, and check balances and pending funds before and after receive operations. <br>
Risk: Private keys, mnemonics, or seeds could be exposed if handled through the agent context. <br>
Mitigation: Do not export mnemonics or seeds, and use OWS-backed wallet operations rather than asking the agent to handle private keys. <br>
Risk: Ambiguous requests using the word Nano may refer to non-XNO products. <br>
Mitigation: Clarify ambiguous requests and use this skill only for the Nano cryptocurrency protocol. <br>


## Reference(s): <br>
- [Nano.org](https://nano.org) <br>
- [ClawHub Skill Page](https://clawhub.ai/cbrunnkvist/skills/nano) <br>
- [xno-skills MCP Reference](references/mcp.md) <br>
- [xno-skills Balance Reference](references/balance.md) <br>
- [xno-skills Send Reference](references/send.md) <br>
- [xno-skills Receive Reference](references/receive.md) <br>
- [xno-skills Address Validation Reference](references/validate.md) <br>
- [xno-skills Unit Conversion Reference](references/convert.md) <br>
- [Blocklattice Representatives](https://blocklattice.io/representatives) <br>
- [Nanoticker Representatives](https://nanoticker.org/representatives) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON MCP tool calls and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce wallet operation plans, Nano addresses, transaction hashes, explorer links, QR output, and JSON tool results when supported by the client.] <br>

## Skill Version(s): <br>
4.4.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
