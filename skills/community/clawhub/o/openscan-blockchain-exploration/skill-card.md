## Description: <br>
Procedural knowledge for on-chain blockchain analysis using the openscan CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matiasos](https://clawhub.ai/user/matiasos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and blockchain analysts use this skill to run OpenScan CLI workflows for transaction history, transaction analysis, gas fees, token balances, and address profiling across supported EVM networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send blockchain lookups, wallet addresses, transaction hashes, or API requests to public or third-party RPC/API providers. <br>
Mitigation: Use a trusted RPC provider for sensitive investigations and avoid sharing unnecessary identifiers or private context in commands. <br>
Risk: RPC and explorer API keys may be exposed if pasted directly into prompts, command history, or logs. <br>
Mitigation: Prefer environment variables or a secret manager for ALCHEMY_API_KEY and ETHERSCAN_API_KEY, and avoid embedding real keys in shared commands. <br>
Risk: Wallet seed phrases or private keys are not required for this read-only analysis workflow and would create severe account risk if disclosed. <br>
Mitigation: Never provide wallet seed phrases or private keys when using this skill. <br>


## Reference(s): <br>
- [OpenScan Explorer GitHub](https://github.com/openscan-explorer) <br>
- [ClawHub Skill Page](https://clawhub.ai/matiasos/openscan-blockchain-exploration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and references to JSON, table, or stream CLI outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should include OpenScan verification links when command output provides them.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
