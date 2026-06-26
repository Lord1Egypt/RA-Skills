## Description: <br>
Nano (XNO) cryptocurrency wallet operations, transaction analysis, and explorer lookups. Use for send/receive, balances, pending funds, address validation, unit conversion, tx/hash/account lookup, explorer links, and Nano block-lattice questions. Prefer xno-mcp first; use xno-skills CLI as fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cbrunnkvist](https://clawhub.ai/user/cbrunnkvist) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate Nano (XNO) wallets, inspect account and transaction state, generate payment requests, validate addresses, convert units, and prepare explorer or RPC lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent real Nano cryptocurrency authority, including wallet receive, send, refund, representative change, spending-limit change, and RPC configuration actions. <br>
Mitigation: Require explicit human approval before any on-chain wallet action, spending-limit update, representative change, or RPC configuration change. <br>
Risk: Automatic receiving of pending Nano funds can publish on-chain blocks without a separate confirmation step. <br>
Mitigation: Gate receive operations behind operator approval unless the deployment policy explicitly allows automatic receiving for the selected wallet. <br>
Risk: The skill should not be used for generic wallet or balance requests that are not clearly about Nano/XNO. <br>
Mitigation: Confirm the request is specifically about Nano, XNO, nano_ or xrb_ addresses, or Nano block-lattice activity before activating the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cbrunnkvist/nano) <br>
- [Nano protocol](https://nano.org) <br>
- [MCP setup reference](references/mcp.md) <br>
- [Send command reference](references/send.md) <br>
- [Receive command reference](references/receive.md) <br>
- [Balance command reference](references/balance.md) <br>
- [Address validation reference](references/validate.md) <br>
- [Unit conversion reference](references/convert.md) <br>
- [Message signing reference](references/sign.md) <br>
- [Message verification reference](references/verify.md) <br>
- [Nano representatives](https://blocklattice.io/representatives) <br>
- [NanoTicker representatives](https://nanoticker.org/representatives) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct an agent to use xno-mcp tools first and xno-skills CLI commands as a fallback.] <br>

## Skill Version(s): <br>
4.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
