## Description: <br>
OpenSoul helps agents implement encrypted, blockchain-based audit logging for persistent memory, self-reflection, and economic activity tracking on Bitcoin SV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MasterGoogler](https://clawhub.ai/user/MasterGoogler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use OpenSoul to add persistent, auditable action logs, session history, performance reflection, and cost tracking to Python-based agents. It is most relevant when an agent needs verifiable records across sessions and the operator is prepared to manage blockchain wallet and encryption keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to handle BSV wallet private keys and PGP private keys. <br>
Mitigation: Use a new low-balance or testnet wallet, store keys outside source control, prefer passphrase-protected PGP keys, and treat local backup JSON files as sensitive records with encryption, restrictive permissions, and deletion policies. <br>
Risk: Agent logs may contain prompts, personal data, secrets, raw queries, document names, or confidential business details that become permanent if written to a public blockchain. <br>
Mitigation: Log only minimal redacted metadata or encrypted commitments, review fields before flushing, and avoid publishing raw prompts, secrets, PII, or confidential business context. <br>
Risk: External install or clone workflows can run code from outside the reviewed artifact. <br>
Mitigation: Audit any cloned repository and external install script before execution, and prefer installing dependencies in an isolated virtual environment. <br>


## Reference(s): <br>
- [OpenSoul on ClawHub](https://clawhub.ai/MasterGoogler/opensoul) <br>
- [MasterGoogler publisher profile](https://clawhub.ai/user/MasterGoogler) <br>
- [Bitcoin SV documentation](https://wiki.bitcoinsv.io/) <br>
- [OpenPGP](https://www.openpgp.org/) <br>
- [WhatsOnChain block explorer](https://whatsonchain.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation guidance and example code; runtime behavior may write local backups and publish encrypted or redacted log data to the BSV blockchain when configured by the operator.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
