## Description:

Guides agents through Openclast/Openclaw wallet setup, balance checks, transactions, approval flows, and key-export safety rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabriziogianni7](https://clawhub.ai/user/fabriziogianni7)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to have an agent help operate an Openclast/Openclaw wallet, including setup, balance queries, transaction preparation, user approvals, and safer handling of key export requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact wallet actions such as sends, approvals, and contract calls.

Mitigation: Keep notify/approval mode enabled, require explicit user approval before broadcast, and use strict per-transaction and daily spending limits.

Risk: Automated sends or broad contract permissions could move funds without enough review if deliberately enabled.

Mitigation: Restrict allowed recipients, chains, and verified contract addresses before enabling automation.

Risk: Private key export can expose wallet credentials.

Mitigation: Avoid exporting private keys unless necessary, require explicit confirmation, and prefer safer recovery or keychain-backed alternatives.

## Reference(s):

- [Openclast Wallet on ClawHub](https://clawhub.ai/fabriziogianni7/skills/openclast-wallet)
- [Publisher profile](https://clawhub.ai/user/fabriziogianni7)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline CLI commands, configuration keys, approval steps, and transaction reference links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance should preserve explicit approval for outgoing transactions unless the wallet configuration deliberately enables auto mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
