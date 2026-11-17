## Description:

Knowbster helps AI agents browse, buy, sell, and validate domain knowledge through a Base L2 cryptocurrency marketplace with REST API, smart contract, and IPFS examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robertoono](https://clawhub.ai/user/robertoono)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent builders use this skill to integrate autonomous agents with Knowbster for discovering, purchasing, listing, and validating marketplace knowledge on Base L2.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use wallet private keys and initiate transactions that spend real ETH.

Mitigation: Use a low-value or test wallet, keep funded private keys out of the agent process, and require explicit human approval before every transaction.

Risk: Uploaded content may be stored through IPFS or Pinata and become difficult to remove.

Mitigation: Do not upload secrets, personal data, regulated data, or proprietary content unless persistence and disclosure are acceptable.

Risk: Dependency installation may pull changing package versions.

Mitigation: Use pinned install commands and locked dependency versions before deployment.

## Reference(s):

- [Knowbster documentation](https://knowbster.com/docs)
- [Knowbster API](https://knowbster.com/api)
- [Knowbster website](https://knowbster.com)
- [Knowbster contract on BaseScan](https://basescan.org/address/0x7cAcb4f7c1d1293DE6346cAde3D27DD68Def6cDA)
- [ClawHub skill page](https://clawhub.ai/robertoono/skills/knowbster)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoints, environment variables, smart contract details, and agent integration examples.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
