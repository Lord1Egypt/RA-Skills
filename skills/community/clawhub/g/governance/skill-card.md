## Description:

Interact with XPR Network on-chain governance: view communities and proposals, inspect votes, cast votes, and create proposals on the gov contract.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulgnz](https://clawhub.ai/user/paulgnz)

### License/Terms of Use:


## Use Case:

Developers, governance operators, and XPR Network participants use this skill to inspect governance state, review proposal details and votes, and perform confirmed on-chain voting or proposal creation actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign irreversible XPR mainnet governance votes and proposal-fee transactions using private-key environment variables.

Mitigation: Use only an account and permission intended for governance actions, prefer a narrowly scoped permission over a general active key, and review proposal IDs, candidates, vote weights, fees, and account details before setting confirmed=true.

Risk: Proposal creation spends the applicable community fee and posts a public on-chain action.

Mitigation: Check the community proposal fee, strategy, voting system, content ID, and voting window against the governance site or API before confirming proposal creation.

Risk: The install metadata does not clearly declare the private-key environment variables required for write operations.

Mitigation: Document XPR_PRIVATE_KEY, XPR_ACCOUNT, and XPR_PERMISSION in deployment procedures and avoid supplying signing credentials when only read-only governance tools are needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulgnz/skills/governance)
- [XPR Network governance website](https://gov.xprnetwork.org)
- [XPR Network governance API](https://gov.api.xprnetwork.org)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [JSON-like tool responses with concise text fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read tools return governance records; write tools return transaction IDs or validation errors after explicit confirmation.]

## Skill Version(s):

0.2.11 (source: server release evidence; artifact skill.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
