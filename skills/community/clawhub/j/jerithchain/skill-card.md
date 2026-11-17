## Description:

Enables an OpenClaw agent to manage a JerithChain wallet, inspect node-reported balances and transactions, send JER, monitor deposits, and request node-side mining.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paradoxfuzzle](https://clawhub.ai/user/paradoxfuzzle)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to create and back up a JER wallet, check on-chain activity, estimate fees, send funds, and monitor transaction confirmations through a configured node.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend JER funds.

Mitigation: Review recipients, fees, configured spending limits, and explicit confirmation before sends.

Risk: Wallet backups contain both the wallet and its key, despite being described as encrypted.

Mitigation: Treat backup archives as wallet-control material; store them offline and never upload or share them.

Risk: The skill accesses a local node token and wallet files, and sends requests to configured RPC and explorer endpoints.

Mitigation: Install only if you trust the skill with these files and credentials, and verify endpoint URLs before use.

## Reference(s):

- [JerithChain skill on ClawHub](https://clawhub.ai/paradoxfuzzle/skills/jerithchain)
- [ClawHub publisher profile](https://clawhub.ai/user/paradoxfuzzle)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or structured JSON (--json)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports node-supplied chain data and transaction confirmation counts.]

## Skill Version(s):

1.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
